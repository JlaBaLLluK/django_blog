from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms import Form, CharField, PasswordInput

from auth_user.models import AuthUser


class LoginForm(Form):
    username_or_email = CharField(required=True, max_length=255)
    password = CharField(required=True, max_length=255, widget=PasswordInput)

    def clean(self):
        super().clean()
        username_or_email = self.cleaned_data.get('username_or_email')
        try:
            if '@' in username_or_email:
                user = AuthUser.objects.get(email=username_or_email)
            else:
                user = AuthUser.objects.get(username=username_or_email)
        except ObjectDoesNotExist:
            raise ValidationError(
                {'username_or_email': ValidationError("User with such username or email doesn't exist!")})

        if not user.check_password(self.cleaned_data.get('password')):
            raise ValidationError({'password': ValidationError('This password is wrong!')})

        return self.cleaned_data
