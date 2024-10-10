from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import FormView
from public_chat.models import PublicChatRoom
from public_chat.forms import ChatmessageCreateForm


class ChatView(LoginRequiredMixin, TemplateView, FormView):
    template_name = 'public_chat/chat.html'
    form_class = ChatmessageCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat_room = get_object_or_404(PublicChatRoom, title=self.kwargs['chatroom_name'])
        chat_messages = chat_room.chat_messeges.all()
        context['chat_messages'] = chat_messages
        context['form'] = self.get_form()  
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if request.htmx and form.is_valid():
            chat_room = get_object_or_404(PublicChatRoom, title='public_chat')
            message = form.save(commit=False)
            message.user_id = request.user
            message.chatroom_id = chat_room
            message.save()
            context = {
                'message': message,
                'user': request.user,
            }
            return render(request, 'public_chat/partials/chat_message_p.html', context)
        
        return self.render_to_response(self.get_context_data(form=form))
