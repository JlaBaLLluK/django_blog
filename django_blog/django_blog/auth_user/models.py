from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db.models import CharField, EmailField


class AuthUser(AbstractUser):
    username = CharField(blank=False, null=False, unique=True, max_length=255,
                         validators=[MinLengthValidator(4, "Username must contain at least 4 symbols!")])
    password = CharField(blank=False, null=False, max_length=255,
                         validators=[MinLengthValidator(8, "Password must contain at least 8 symbols!")])
    email = EmailField(blank=False, null=False, unique=True, max_length=255)

    class Meta:
        db_table = 'Users'
