from django.db.models.signals import post_save
from django.dispatch import receiver
from videos.models import History 
from videos.models import Video
from public_chat.models import PublicChatRoom
from django.contrib.auth.models import User
from django.utils import timezone

@receiver(post_save, sender=Video)
def create_history(sender, instance, created, **kwargs):
    print('yes')
    request = kwargs.get('request')
    user = request.user if request else None

    if user and user.is_authenticated:
        History.objects.create(
            user_id=user.id,
            video_id=instance,
            watch_date=timezone.now()
        )

@receiver(post_save, sender=Video)
def create_chat_room(sender, instance, created, **kwargs):
    if created:
        PublicChatRoom.objects.create(
            title=f"{instance.name}",
            video_id=instance
        )
