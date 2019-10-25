from django.contrib import admin
from .models import Blog, Attachment, Comment, CommentReply

class BlogAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'category', 'slug', 'tags']

    class Meta:
        model = Blog


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['blog', 'file', 'slug', 'created_at']

    class Meta:
        model = Attachment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['blog', 'commented_by', 'is_selected', 'created_at']

    class Meta:
        model = Comment


class CommentReplyAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'replied_by', 'created_at']

    class Meta:
        model = CommentReply


admin.site.register(Blog, BlogAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentReply, CommentReplyAdmin)
