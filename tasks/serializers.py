from rest_framework import serializers
from django.utils import timezone
from .models import Task
import re


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'due_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'title': {
                'required': True,
                'max_length': 255,
                'help_text': 'Task title (required, max 255 characters)'
            },
            'description': {
                'required': False,
                'allow_blank': True,
                'help_text': 'Detailed task description (optional)'
            },
            'status': {
                'required': False,
                'help_text': 'Task status: pending or completed'
            },
            'priority': {
                'required': False,
                'help_text': 'Task priority: low, medium, or high'
            },
            'due_date': {
                'required': False,
                'allow_null': True,
                'help_text': 'Task due date and time (optional, must be in the future)'
            }
        }
    
    def validate_title(self, value):
        """
        Validate task title
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Task title is required and cannot be empty.")
        
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Task title must be at least 3 characters long.")
        
        if len(value) > 255:
            raise serializers.ValidationError("Task title cannot exceed 255 characters.")
        
        # Check for only special characters
        if not re.search(r'[a-zA-Z0-9]', value):
            raise serializers.ValidationError("Task title must contain at least one letter or number.")
        
        return value.strip()
    
    def validate_description(self, value):
        """
        Validate task description if provided
        """
        if value and len(value) > 5000:
            raise serializers.ValidationError("Task description cannot exceed 5000 characters.")
        
        return value.strip() if value else value
    
    def validate_status(self, value):
        """
        Validate task status
        """
        valid_statuses = ['pending', 'completed']
        if value and value not in valid_statuses:
            raise serializers.ValidationError(
                f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )
        return value
    
    def validate_priority(self, value):
        """
        Validate task priority
        """
        valid_priorities = ['low', 'medium', 'high']
        if value and value not in valid_priorities:
            raise serializers.ValidationError(
                f"Invalid priority. Must be one of: {', '.join(valid_priorities)}"
            )
        return value
    
    def validate_due_date(self, value):
        """
        Validate that due date is not in the past
        """
        if value:
            # Remove timezone info for comparison if needed
            now = timezone.now()
            
            # Check if due date is in the past
            if value < now:
                raise serializers.ValidationError(
                    "Due date cannot be in the past. Please select today or a future date."
                )
            
            # Check if due date is too far in the future (e.g., more than 10 years)
            max_future_date = now + timezone.timedelta(days=3650)  # 10 years
            if value > max_future_date:
                raise serializers.ValidationError(
                    "Due date cannot be more than 10 years in the future."
                )
        
        return value
    
    def validate(self, attrs):
        """
        Object-level validation
        """
        # If status is being set to completed, ensure task has a title
        if attrs.get('status') == 'completed':
            title = attrs.get('title') or (self.instance.title if self.instance else None)
            if not title:
                raise serializers.ValidationError({
                    "status": "Cannot mark task as completed without a title."
                })
        
        # Validate priority is set (default to medium if not provided)
        if 'priority' not in attrs and not self.instance:
            attrs['priority'] = 'medium'
        
        # Validate status is set (default to pending if not provided)
        if 'status' not in attrs and not self.instance:
            attrs['status'] = 'pending'
        
        return attrs
