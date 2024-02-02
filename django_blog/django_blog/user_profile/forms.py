from django.core.exceptions import ObjectDoesNotExist
from django.forms import Form, CharField, EmailField

from auth_user.models import AuthUser


class EditProfileDataForm(Form):
    username = CharField(max_length=255, required=True, min_length=4)
    email = EmailField(max_length=255, required=True)
    first_name = CharField(max_length=255, required=False)
    last_name = CharField(max_length=255, required=False)

    def check_if_new_data_correct(self, user):
        try:
            user_obj = AuthUser.objects.get(username=self.cleaned_data.get('username'))
        except ObjectDoesNotExist:
            pass
        else:
            if user_obj.username != user.username:
                self.add_error('username', 'This username is already taken!')
                return False

        try:
            user_obj = AuthUser.objects.get(email=self.cleaned_data.get('email'))
        except ObjectDoesNotExist:
            pass
        else:
            if user_obj.email != user.email:
                self.add_error('email', 'This email is already taken!')
                return False

        return True
