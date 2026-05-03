from django.contrib import admin

from app_quiz.models import Option, Participant, Question, Quiz, QuizResult


class OptionInline(admin.TabularInline):
    model = Option
    extra = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'quiz')
    list_filter = ('quiz',)
    search_fields = ('question',)
    inlines = [OptionInline]


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title', 'description')


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('option', 'question', 'is_correct')
    list_filter = ('is_correct', 'question__quiz')
    search_fields = ('option',)


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_class', 'age', 'gender', 'institution', 'user')
    search_fields = ('name', 'institution', 'user__username')


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('participant', 'quiz', 'score', 'total_questions', 'submitted_at')
    list_filter = ('quiz',)
    search_fields = ('participant__name', 'quiz__title')
