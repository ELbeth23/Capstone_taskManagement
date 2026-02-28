from rest_framework import serializers
from django.utils import timezone
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'due_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_due_date(self, value):
        """
        Validate that due date is not in the past
        """
        if value and value < timezone.now():
            raise serializers.ValidationError(
                "Due date cannot be in the past. Please select today or a future date."
            )
        return value
