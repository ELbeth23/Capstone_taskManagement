from django.contrib import admin
from .models import UserPreferences


@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ('user', 'dark_mode', 'default_priority', 'updated_at')
    list_filter = ('dark_mode', 'default_priority')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
