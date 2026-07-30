
#  for authentication
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import CustomUser

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'user_type',
            'password1',
            'password2',
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for x in self.fields.values():
            x.widget.attrs.update({
                'class': 'form-control'
            })

    def save(self, commit=True):
        user = super().save(commit=False)

        if self.cleaned_data['user_type'] == CustomUser.UserType.QUIZMAKER:
            user.is_staff = True

        if commit:
            user.save()

        return user

class LoginForm(AuthenticationForm):
    username = AuthenticationForm.base_fields['username']
    username.label = 'Username or Email'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for x in self.fields.values():
            x.widget.attrs.update({
                'class': 'form-control'
            })

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and '@' in username:
            user = CustomUser.objects.filter(email__iexact=username).first()
            if not user:
                raise ValidationError('No account exists with this email address.')
            return user.username
        return username
