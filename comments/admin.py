from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'is_active', 'likes_count', 'created_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('content', 'author__username', 'post__title')
    autocomplete_fields = ('author', 'post', 'likes')
    readonly_fields = ('likes_count', 'created_at', 'updated_at')
    ordering = ('-created_at',)
