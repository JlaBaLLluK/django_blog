from django.core.exceptions import ObjectDoesNotExist
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

    # def clean(self):
    #     cleaned_data = super().clean()
    #     try:
    #         user_obj = AuthUser.objects.get(username=cleaned_data.get('username'))
    #     except ObjectDoesNotExist:
    #         pass
    #     else:
    #         if user_obj.username != self.user.username:
    #             self.add_error('username', 'This username is already taken!')
    #             return False
    #
    #     try:
    #         user_obj = AuthUser.objects.get(email=cleaned_data.get('email'))
    #     except ObjectDoesNotExist:
    #         pass
    #     else:
    #         if user_obj.email != self.user.email:
    #             self.add_error('email', 'This email is already taken!')
    #             return False
    #
    #     return True
