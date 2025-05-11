from django.contrib import admin
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'role', 'is_verified', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    list_filter = ('role', 'is_verified', 'is_active', 'is_staff')
    exclude = ('date_joined',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'get_followers_count', 'get_following_count')
    search_fields = ('user__email', 'bio')
    readonly_fields = ('get_followers_count', 'get_following_count')

    def get_followers_count(self, obj):
        return obj.followers.count()
    get_followers_count.short_description = 'Количество подписчиков'

    def get_following_count(self, obj):
        return obj.following.count()
    get_following_count.short_description = 'Количество подписок'
