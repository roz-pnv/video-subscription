from django.urls import path
from public_chat.views import ChatView

urlpatterns = [
    path('', ChatView.as_view(), name='room')
]
