from django.core.exceptions import ValidationError
from django.forms import ModelForm, PasswordInput, CharField, TextInput, EmailInput, Form

from auth_user.models import AuthUser


class RegistrationForm(ModelForm):
    password_confirm = CharField(required=True, max_length=255,
                                 widget=PasswordInput(attrs={'class': 'password-confirm-input'}))

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

    def clean(self):
        super().clean()
        if self.cleaned_data.get('password') != self.cleaned_data.get('password_confirm'):
            raise ValidationError({'password_confirm': ValidationError("Passwords must be same!")})

        return self.cleaned_data

    def save(self, commit=True):
        AuthUser.objects.create_user(username=self.cleaned_data.get('username'),
                                     email=self.cleaned_data.get('email'),
                                     password=self.cleaned_data.get('password'),
                                     is_active=False)


class VerificationForm(Form):
    digit_one = CharField(max_length=1, required=True, widget=TextInput(attrs={'class': 'digit_one'}))
    digit_two = CharField(max_length=1, required=True, widget=TextInput(attrs={'class': 'digit_two'}))
    digit_three = CharField(max_length=1, required=True, widget=TextInput(attrs={'class': 'digit_three'}))
    digit_four = CharField(max_length=1, required=True, widget=TextInput(attrs={'class': 'digit_four'}))
    digit_five = CharField(max_length=1, required=True, widget=TextInput(attrs={'class': 'digit_five'}))
    digit_six = CharField(max_length=1, required=True, widget=TextInput(attrs={'class': 'digit_six'}))
