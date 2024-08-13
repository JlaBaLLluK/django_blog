from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.core.management.commands import check
from django.forms import CharField, EmailField, ModelForm, Form, PasswordInput

from auth_user.models import AuthUser


class EditProfileDataForm(ModelForm):
    username = CharField(max_length=255, required=True, min_length=4)
    email = EmailField(max_length=255, required=True)
    first_name = CharField(max_length=255, required=False)
    last_name = CharField(max_length=255, required=False)

    class Meta:
        model = AuthUser
        fields = ['username', 'first_name', 'last_name', 'email']


class DeleteProfileForm(Form):
    password = CharField(max_length=255, required=True, widget=PasswordInput)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not check_password(password, self.user.password):
            raise ValidationError("Couldn't delete account. This password is wrong!")

        return password
