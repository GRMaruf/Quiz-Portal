from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory

from app_quiz.models import Option, Participant, Question, Quiz


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'student_class', 'age', 'gender', 'institution']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].widget.attrs.update({'class': 'form-control'})


class BaseOptionFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        if any(self.errors):
            return

        filled_options = 0
        correct_options = 0

        for form in self.forms:
            if not hasattr(form, 'cleaned_data') or not form.cleaned_data:
                continue
            if self.can_delete and form.cleaned_data.get('DELETE'):
                continue

            option_text = form.cleaned_data.get('option')
            if option_text:
                filled_options += 1
                if form.cleaned_data.get('is_correct'):
                    correct_options += 1

        if filled_options < 2:
            raise forms.ValidationError('Add at least two options for this question.')

        if correct_options != 1:
            raise forms.ValidationError('Select exactly one correct option.')


OptionFormSet = inlineformset_factory(
    Question,
    Option,
    formset=BaseOptionFormSet,
    fields=['option', 'is_correct'],
    extra=4,
    can_delete=True,
    widgets={
        'option': forms.TextInput(attrs={'class': 'form-control'}),
        'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    },
)
