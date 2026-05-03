from django.urls import path

from app_quiz.views import (
    dashboard,
    home,
    panel_quiz_questions,
    participant_profile,
    question_create,
    question_delete,
    question_edit,
    quiz_create,
    quiz_delete,
    quiz_edit,
    quiz_panel,
    quiz_result,
    take_quiz,
)


urlpatterns = [
    path('', home, name='home'),
    path('profile/', participant_profile, name='participant_profile'),
    path('dashboard/', dashboard, name='dashboard'),
    path('quiz/<int:quiz_id>/', take_quiz, name='take_quiz'),
    path('quiz/<int:quiz_id>/result/', quiz_result, name='quiz_result'),
    path('quiz-panel/', quiz_panel, name='quiz_panel'),
    path('quiz-panel/quizzes/new/', quiz_create, name='quiz_create'),
    path('quiz-panel/quizzes/<int:quiz_id>/edit/', quiz_edit, name='quiz_edit'),
    path('quiz-panel/quizzes/<int:quiz_id>/delete/', quiz_delete, name='quiz_delete'),
    path('quiz-panel/quizzes/<int:quiz_id>/questions/', panel_quiz_questions, name='panel_quiz_questions'),
    path('quiz-panel/quizzes/<int:quiz_id>/questions/new/', question_create, name='question_create'),
    path('quiz-panel/questions/<int:question_id>/edit/', question_edit, name='question_edit'),
    path('quiz-panel/questions/<int:question_id>/delete/', question_delete, name='question_delete'),
]
