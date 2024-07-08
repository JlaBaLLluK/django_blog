from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms import Form, CharField, PasswordInput

from auth_user.models import AuthUser
from auth_user.validators import validate_password_for_strength


class LoginForm(Form):
    username_or_email = CharField(required=True, max_length=255)
    password = CharField(required=True, max_length=255, widget=PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        user = self.validate_username_or_email()
        if not user.check_password(cleaned_data.get('password')):
            raise ValidationError({'password': ValidationError('This password is wrong!')})

        return cleaned_data

    def validate_username_or_email(self):
        username_or_email = self.cleaned_data.get('username_or_email')
        try:
            if '@' in username_or_email:
                user = AuthUser.objects.get(email=username_or_email)
            else:
                user = AuthUser.objects.get(username=username_or_email)
        except ObjectDoesNotExist:
            raise ValidationError(
                {'username_or_email': ValidationError("User with such username or email doesn't exist!")})

        return user


class ResetPasswordForm(LoginForm):
    password = None

    class Meta:
        fields = ['username_or_email']

    def clean(self):
        self.validate_username_or_email()
        return self.cleaned_data


class SetNewPasswordForm(Form):
    password = CharField(required=True, max_length=255, widget=PasswordInput,
                         validators=[validate_password_for_strength], min_length=8)
    password_confirm = CharField(required=True, max_length=255, widget=PasswordInput, min_length=8)

    def clean(self):
        super().clean()
        if self.cleaned_data.get('password') != self.cleaned_data.get('password_confirm') and self.cleaned_data.get(
                'password') is not None:
            raise ValidationError({'password_confirm': ValidationError("Passwords must be same!")})

        return self.cleaned_data
