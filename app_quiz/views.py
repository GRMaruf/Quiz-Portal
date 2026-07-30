from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from app_quiz.forms import OptionFormSet, ParticipantForm, QuestionForm, QuizForm
from app_quiz.models import Option, Participant, Question, Quiz, QuizResult


def staff_required(view_func):
    return login_required(user_passes_test(lambda user: user.is_staff)(view_func))


def home(request):
    return render(request, 'home.html')


@login_required
def participant_profile(request):
    participant = Participant.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.user = request.user
            participant.save()
            return redirect('dashboard')
    else:
        form = ParticipantForm(instance=participant)

    return render(request, 'participant_form.html', {'form': form})


@login_required
def dashboard(request):
    participant = Participant.objects.filter(user=request.user).first()
    if not participant:
        return redirect('participant_profile')

    quizzes = Quiz.objects.all()
    results = QuizResult.objects.filter(participant=participant).select_related('quiz')
    result_map = {result.quiz_id: result for result in results}
    quiz_items = [{'quiz': quiz, 'result': result_map.get(quiz.id)} for quiz in quizzes]

    return render(request, 'dashboard.html', {
        'participant': participant,
        'quiz_items': quiz_items,
    })


@login_required
def take_quiz(request, quiz_id):
    participant = get_object_or_404(Participant, user=request.user)
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    if request.method == 'POST':
        questions = quiz.questions.prefetch_related('options')
        total_questions = questions.count()
        score = 0

        for question in questions:
            selected_option_id = request.POST.get(f'question_{question.id}')
            if selected_option_id and Option.objects.filter(
                id=selected_option_id,
                question=question,
                is_correct=True,
            ).exists():
                score += 1

        QuizResult.objects.update_or_create(
            participant=participant,
            quiz=quiz,
            defaults={'score': score, 'total_questions': total_questions},
        )
        return redirect('quiz_result', quiz_id=quiz.id)

    questions = []
    for question in quiz.questions.order_by('?'):
        question.random_options = question.options.order_by('?')
        questions.append(question)

    return render(request, 'take_quiz.html', {'quiz': quiz, 'questions': questions})


@login_required
def quiz_result(request, quiz_id):
    participant = get_object_or_404(Participant, user=request.user)
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    result = get_object_or_404(QuizResult, participant=participant, quiz=quiz)
    ranked_results = QuizResult.objects.filter(quiz=quiz).order_by('-score', 'submitted_at', 'id')
    position = list(ranked_results.values_list('id', flat=True)).index(result.id) + 1

    return render(request, 'quiz_result.html', {
        'quiz': quiz,
        'result': result,
        'position': position,
        'ranked_results': ranked_results,
    })


@staff_required
def quiz_panel(request):
    quizzes = Quiz.objects.filter(user=request.user).prefetch_related('questions').order_by('title')
    return render(request, 'quiz_panel.html', {'quizzes': quizzes})


@staff_required
def quiz_create(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.user = request.user
            quiz.save()
            messages.success(request, 'Quiz created. Add questions now.')
            return redirect('panel_quiz_questions', quiz_id=quiz.id)
    else:
        form = QuizForm()

    return render(request, 'quiz_form.html', {
        'form': form,
        'title': 'Create Quiz',
        'submit_label': 'Create Quiz',
    })


@staff_required
def quiz_edit(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quiz updated.')
            return redirect('panel_quiz_questions', quiz_id=quiz.id)
    else:
        form = QuizForm(instance=quiz)

    return render(request, 'quiz_form.html', {
        'form': form,
        'quiz': quiz,
        'title': 'Edit Quiz',
        'submit_label': 'Save Changes',
    })


@staff_required
def panel_quiz_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz.objects.prefetch_related('questions__options'), pk=quiz_id)
    return render(request, 'quiz_questions.html', {'quiz': quiz})


@staff_required
def question_create(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    question = Question(quiz=quiz)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = OptionFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                question = form.save()
                formset.instance = question
                formset.save()
            messages.success(request, 'Question added.')
            return redirect('panel_quiz_questions', quiz_id=quiz.id)
    else:
        form = QuestionForm(instance=question)
        formset = OptionFormSet(instance=question, queryset=Option.objects.none())

    return render(request, 'question_form.html', {
        'form': form,
        'formset': formset,
        'quiz': quiz,
        'title': 'Add Question',
        'submit_label': 'Add Question',
    })


@staff_required
def question_edit(request, question_id):
    question = get_object_or_404(Question.objects.select_related('quiz'), pk=question_id)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = OptionFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, 'Question updated.')
            return redirect('panel_quiz_questions', quiz_id=question.quiz_id)
    else:
        form = QuestionForm(instance=question)
        formset = OptionFormSet(instance=question)

    return render(request, 'question_form.html', {
        'form': form,
        'formset': formset,
        'quiz': question.quiz,
        'question': question,
        'title': 'Edit Question',
        'submit_label': 'Save Changes',
    })


@staff_required
@require_POST
def quiz_delete(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    quiz.delete()
    messages.success(request, 'Quiz deleted.')
    return redirect('quiz_panel')


@staff_required
@require_POST
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    quiz_id = question.quiz_id
    question.delete()
    messages.success(request, 'Question deleted.')
    return redirect('panel_quiz_questions', quiz_id=quiz_id)
