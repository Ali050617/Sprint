from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator

from django.core.mail import EmailMultiAlternatives
from rest_framework.exceptions import ValidationError
from .models import User


# def send_verification_email(user):
#     if not user.verification_token:
#         return
#
#     message = f'Please verify your email using this token:{user.verification_token}'
#
#
#     send_mail(
#         subject='Email Verification',
#         message=message,
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[user.email],
#         fail_silently=False
#     )


def generate_reset_token(user):
    return default_token_generator.make_token(user)


def send_password_reset_email(user):
    token = generate_reset_token(user)
    subject = "Сброс пароля"
    from_email = "support@yourdomain.com"
    to_email = [user.email]

    html_content = render_to_string('emails/password_reset_email.html', {
        'user': user,
        'token': token
    })

    text_content = f"Ваш токен для сброса пароля: {token}"
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def reset_password_confirm(data):
    token = data['token']
    password = data['password']
    password_confirm = data['password_confirm']

    if password != password_confirm:
        raise ValidationError("Пароли не совпадают.")

    user = next((u for u in User.objects.iterator() if default_token_generator.check_token(u, token)), None)
    if not user:
        raise ValidationError("Токен недействителен или истёк срок его действия.")

    user.set_password(password)
    user.save()
    return {"detail": "Пароль успешно обновлён."}

