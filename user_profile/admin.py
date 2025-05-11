from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'username', 'role', 'is_verified', 'is_active', 'is_staff')
    list_filter = ('role', 'is_verified', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    ordering = ('-date_joined',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'get_followers_count', 'get_following_count')
    search_fields = ('user__email', 'bio')
    readonly_fields = ('get_followers_count', 'get_following_count')

    def get_followers_count(self, obj):
        return obj.followers.count()
    get_followers_count.short_description = 'Количество подписчиков'

    def get_following_count(self, obj):
        return obj.user.user_profile.following.count()
    get_following_count.short_description = 'Количество подписок'
