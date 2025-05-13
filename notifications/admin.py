from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'actor', 'verb', 'target_type', 'target_id', 'is_read', 'created_at')
    list_filter = ('is_read', 'verb', 'target_type', 'created_at')
    search_fields = ('recipient__username', 'actor__username', 'verb')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('recipient', 'actor')