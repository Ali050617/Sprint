from rest_framework.exceptions import ValidationError


def reset_password_confirm(data):
    token = data['token']
    password = data['password']
    password_confirm = data['password_confirm']

    if password != password_confirm:
        raise ValidationError("Пароли не совпадают.")

    return {"detail": "Пароль успешно изменён."}