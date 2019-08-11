from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from el_pagination.decorators import page_template
from chat.models import Thread
from django.db.models import Q


class HomeView(TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user
        # Starts Base Template Context
        if self.request.user.is_superuser:
            base_template = 'admin-site/base.html'
        else:
            base_template = 'base.html'
        # Ends Base Template Context
        context = {
            'base_template': base_template
        }
        if user.is_superuser:
            return render(request, "admin-site/pages/home.html", context=context)
        return render(request, "pages/home.html", context=context)


# @method_decorator(login_required, name='dispatch')
# class ChatListTemplateView(TemplateView):
#     def get(self, request, *args, **kwargs):
#         return render(request, "chat/chat-list.html")


@login_required
@page_template('chat/snippets/list.html')
def get_chat_list_template(request,
                           template='chat/chat-list.html',
                           extra_context=None):
    chat_list = None
    qs = Thread.objects.filter(Q(first=request.user) | Q(second=request.user))
    if qs.exists():
        chat_list = qs.order_by('-updated_at')
    # Starts Base Template Context
    if request.user.is_superuser:
        base_template = 'admin-site/base.html'
    else:
        base_template = 'base.html'
    # Ends Base Template Context
    context = {
        'chat_list': chat_list,
        'base_template': base_template
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)
