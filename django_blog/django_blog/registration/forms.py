from django.core.exceptions import ValidationError
from django.forms import ModelForm, PasswordInput, CharField, TextInput, EmailInput

from auth_user.models import AuthUser


class RegistrationForm(ModelForm):
    password_confirm = CharField(required=True, max_length=255,
                                 widget=PasswordInput(attrs={'class': 'password-confirm-input'}))

    def clean(self):
        super().clean()
        if self.cleaned_data.get('password') != self.cleaned_data.get('password_confirm'):
            raise ValidationError({'password_confirm': ValidationError("Passwords must be same!")})

        return self.cleaned_data

    class Meta:
        model = AuthUser
        fields = ['username', 'password', 'password_confirm', 'email']
        widgets = {
            'username': TextInput(attrs={'class': 'username-input'}),
            'password': PasswordInput(attrs={'class': 'password-input'}),
            'email': EmailInput(attrs={'class': 'email-input'})
        }
        error_messages = {
            'username': {
                'unique': 'This username is already taken!',
            },
            'email': {
                'unique': 'This email is already taken!',
            }
        }
