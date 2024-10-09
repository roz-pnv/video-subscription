from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from videos.models import Video
from datetime import datetime

class PublicChatRoom(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
    )
    video_id = models.OneToOneField(
        Video,
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
        return self.title
    

class PublicChatRoomMessage(models.Model):
    chatroom_id = models.ForeignKey(
        PublicChatRoom,
        on_delete=models.CASCADE,
        related_name='chat_messeges',
    )
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    body = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        dt = datetime.strptime(str(self.created_at), "%Y-%m-%d %H:%M:%S.%f%z")
        time_only = dt.strftime("%H:%M")      
        return f'{self.user_id.username}: "{self.body}" at {time_only}'
    
    class Meta:
        ordering = ['-created_at']
