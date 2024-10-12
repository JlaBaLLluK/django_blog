from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.forms import CharField, ModelForm, Form, PasswordInput

from auth_user.models import AuthUser


class EditProfileDataForm(ModelForm):

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
