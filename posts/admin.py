from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'is_active', 'likes_count', 'comments_count', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    ordering = ('-created_at',)
