from django.contrib import admin
from .models import UserPreferences


@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_notifications', 'task_reminders', 'daily_summary', 'default_priority', 'updated_at')
    list_filter = ('email_notifications', 'task_reminders', 'daily_summary', 'default_priority')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')

