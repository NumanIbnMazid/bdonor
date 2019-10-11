from django.contrib import admin
from .models import Blog, Attachment

class BlogAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'slug']

    class Meta:
        model = Blog


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['blog', 'file']

    class Meta:
        model = Attachment


admin.site.register(Blog, BlogAdmin)
admin.site.register(Attachment, AttachmentAdmin)
