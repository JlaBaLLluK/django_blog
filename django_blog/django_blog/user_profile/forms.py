from django.forms import CharField, EmailField, ModelForm

from auth_user.models import AuthUser


class EditProfileDataForm(ModelForm):
    username = CharField(max_length=255, required=True, min_length=4)
    email = EmailField(max_length=255, required=True)
    first_name = CharField(max_length=255, required=False)
    last_name = CharField(max_length=255, required=False)

    class Meta:
        model = AuthUser
        fields = ['username', 'first_name', 'last_name', 'email']
