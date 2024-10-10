from django.urls import re_path
from public_chat.consumers import ChatroomConsumer

websocket_urlpatterns = [
    re_path('ws/chatroom/(?P<chatroom_name>\w+)/$', ChatroomConsumer.as_asgi())
]
