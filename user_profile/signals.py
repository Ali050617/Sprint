import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save
from .models import User, UserProfile
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def send_verification_email_on_create(sender, instance, created, **kwargs):
    if created and not instance.is_verified:
        token = get_random_string(64)
        instance.email_token = token
        instance.save()

        message = f"Пожалуйста, подтвердите вашу почту, используя этот токен:\n\n{token}"
        send_mail(
            subject='Подтверждение электронной почты',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.email],
            fail_silently=False,
        )


@receiver(post_delete, sender=UserProfile)
def delete_user_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=UserProfile)
def delete_old_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = UserProfile.objects.get(pk=instance.pk)
    except UserProfile.DoesNotExist:
        return

    old_image = old_instance.image
    new_image = instance.image

    if old_image and old_image != new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)


