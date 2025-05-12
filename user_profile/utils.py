from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(user):
    verification_link = f"http://localhost:8000/auth/verify-email/?token={user.email_token}"
    send_mail(
        subject="Подтверждение email",
        message=f"Пожалуйста, подтвердите ваш email, перейдя по ссылке: {verification_link}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )