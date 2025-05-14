import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.db.models.signals import post_delete, pre_save
from .models import User, UserProfile
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings


# AUTO CREATE USER PROFILE
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# VERIFY EMAIL
@receiver(post_save, sender=User)
def send_verification_email_on_create(sender, instance, created, **kwargs):
    if created and not instance.is_verified:
        instance.email_token = instance.email_token or get_random_string(32)
        instance.save()

        message = render_to_string('emails/verify_email.html', {
            'token': instance.email_token,
        })

        send_mail(
            subject='Подтверждение электронной почты',
            message='',
            html_message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.email],
            fail_silently=False,
        )

# IMAGE UPDATE
@receiver(pre_save, sender=UserProfile)
def delete_old_image_on_update(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = UserProfile.objects.get(pk=instance.pk)

            if old_instance.image and (not instance.image or old_instance.image != instance.image):
                if os.path.isfile(old_instance.image.path):
                    os.remove(old_instance.image.path)
        except UserProfile.DoesNotExist:
            pass

# IMAGE DELETE
@receiver(post_delete, sender=UserProfile)
def delete_image_on_profile_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)