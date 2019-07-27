
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView, get_chat_list_template

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('account/', include('accounts.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('chat/', include('chat.urls')),
    path('chat-messages/', get_chat_list_template, name='chat_list'),
    path('utils/', include(('utils.urls', 'utils'), namespace='utils')),
    path('donations/', include(('donations.urls', 'donations'), namespace='donations')),
]


if settings.DEBUG:
    urlpatterns = urlpatterns + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
