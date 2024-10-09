from django.contrib import admin
from public_chat.models import PublicChatRoom
from public_chat.models import PublicChatRoomMessage

admin.site.register(PublicChatRoom)
admin.site.register(PublicChatRoomMessage)
