from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db.models import CharField, EmailField
from auth_user.validators import *


class AuthUser(AbstractUser):
    username = CharField(blank=False, null=False, unique=True, max_length=255,
                         validators=[MinLengthValidator(4, "Username must contain at least 4 symbols!"),
                                     validate_username_for_forbidden_symbols])
    password = CharField(blank=False, null=False, max_length=255,
                         validators=[MinLengthValidator(8, "Password must contain at least 8 symbols!"),
                                     validate_password_for_strength],)
    email = EmailField(blank=False, null=False, unique=True)

    class Meta:
        db_table = 'Users'
