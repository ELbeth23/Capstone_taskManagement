from django.db import models
from django.contrib.auth.models import User


class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    
    # Profile image
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    
    # Notification preferences
    email_notifications = models.BooleanField(default=False)
    task_reminders = models.BooleanField(default=True)
    daily_summary = models.BooleanField(default=False)
    
    # Appearance settings
    dark_mode = models.BooleanField(default=False)
    
    # Default task settings
    default_priority = models.CharField(
        max_length=10,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='medium'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s preferences"

    class Meta:
        verbose_name_plural = "User Preferences"
