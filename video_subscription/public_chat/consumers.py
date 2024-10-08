from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from public_chat.models import PublicChatRoom
from public_chat.models import PublicChatRoomMessage
from asgiref.sync import async_to_sync
import json

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(PublicChatRoom, title=self.chatroom_name)

        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name, self.channel_name
        )

        if self.user not in self.chatroom.user_id.all():
            self.chatroom.user_id.add(self.user) 
            self.update_user_id()

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name, self.channel_name
        )

        if self.user  in self.chatroom.user_id.all():
            self.chatroom.user_id.remove(self.user) 
            self.update_user_id()

    def receive(self, text_data):
        data = json.loads(text_data)
        body= data['body']

        message = PublicChatRoomMessage.objects.create(
            body = body,
            user_id = self.user,
            chatroom_id = self.chatroom,
        )
        message.save()

        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )
    
    def message_handler(self, event):
        message_id = event['message_id']
        message = PublicChatRoomMessage.objects.get(id=message_id)
        context = {
            'message' : message,
            'user' : self.user,
        }
        html = render_to_string('public_chat/partials/chat_message_p.html', context=context)

        self.send(text_data=html)

    def update_user_id(self):
        online_count = self.chatroom.user_id.count()

        event = {
            'type': 'online_count_handler',
            'online_count': online_count,
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )

    def online_count_handler(self, event):
        online_count = event['online_count']
        html = render_to_string('public_chat/partials/online_count.html', {'online_count' : online_count})
        self.send(text_data=html) 
