from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField


class AuthUser(AbstractUser):
    username = CharField(blank=False, null=False, unique=True, max_length=255)
    password = CharField(blank=False, null=False, max_length=255)
    email = EmailField(blank=False, null=False, unique=True, max_length=255)

    class Meta:
        db_table = 'Users'
