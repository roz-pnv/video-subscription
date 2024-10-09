from django.forms import ModelForm
from django import forms
from public_chat.models import PublicChatRoom
from public_chat.models import PublicChatRoomMessage

class ChatmessageCreateForm(ModelForm):
    class Meta:
        model = PublicChatRoomMessage
        fields = ['body']
        widgets = {
            'body': forms.TextInput(
                attrs={
                    'placeholder': 'Add message ...',
                    'class': 'p-4 text-black',
                    'maxlength': '300',
                    'autofocus': True,
                },
            ), 
        }
