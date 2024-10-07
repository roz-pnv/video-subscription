from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from videos.models import Subscription


# @receiver(pre_save, sender=User)
# def reset_verifications_on_change(sender, instance, **kwargs):
#     if instance.pk:
#         old_user = User.objects.get(pk=instance.pk)

#         if old_user.phone != instance.phone:
#             instance.is_phone_verified = False

#         if old_user.email != instance.email:
#             instance.is_email_verified = False


@receiver(post_save, sender=User)
def create_default_subscription(sender, instance, created, **kwargs):
    if created:
        Subscription.objects.create(
            user_id=instance, 
            type=Subscription.TypeChoices.NORMAL, 
            status=Subscription.StatusChoices.DIACTIVE,
        )
