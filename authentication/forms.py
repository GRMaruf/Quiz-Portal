
#  for authentication
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for x in self.fields.values():
            x.widget.attrs.update({
                'class': 'form-control'
            })

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
            user = User.objects.filter(email__iexact=username).first()
            if not user:
                raise ValidationError('No account exists with this email address.')
            return user.username
        return username
