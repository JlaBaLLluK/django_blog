from django.core.exceptions import ValidationError


def validate_username_for_forbidden_symbols(username):
    forbidden_symbols = ' ~`!@#№$;%:^&*()-=+/*\\]}[{"<>' + "'"
    for char in username:
        if char in forbidden_symbols:
            raise ValidationError("Username contains forbidden symbol. Use letters, digits and underscores!")


def validate_password_for_strength(password):
    if password.isdigit():
        raise ValidationError("Password can't contain only digits!")
