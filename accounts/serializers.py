from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from .models import UserPreferences
import re


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        min_length=8,
        style={'input_type': 'password'},
        help_text="Password must be at least 8 characters long"
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'},
        help_text="Re-enter your password for confirmation"
    )
    email = serializers.EmailField(
        required=True,
        validators=[EmailValidator(message="Enter a valid email address")],
        help_text="Valid email address required"
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'username': {
                'required': True,
                'min_length': 3,
                'max_length': 150,
                'help_text': 'Username must be 3-150 characters. Letters, digits and @/./+/-/_ only.'
            },
            'first_name': {
                'required': False,
                'max_length': 150,
                'allow_blank': True
            },
            'last_name': {
                'required': False,
                'max_length': 150,
                'allow_blank': True
            }
        }

    def validate_username(self, value):
        """
        Validate username format and uniqueness
        """
        # Check if username is empty or only whitespace
        if not value or not value.strip():
            raise serializers.ValidationError("Username cannot be empty or contain only spaces.")
        
        # Check length
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters long.")
        
        if len(value) > 150:
            raise serializers.ValidationError("Username cannot exceed 150 characters.")
        
        # Check for valid characters (alphanumeric, @, ., +, -, _)
        if not re.match(r'^[\w.@+-]+$', value):
            raise serializers.ValidationError(
                "Username can only contain letters, numbers, and @/./+/-/_ characters."
            )
        
        # Check if username already exists (case-insensitive)
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        
        return value.strip()

    def validate_email(self, value):
        """
        Validate email format and uniqueness
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Email address is required.")
        
        # Check if email already exists (case-insensitive)
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email address already exists.")
        
        # Additional email format validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Enter a valid email address.")
        
        return value.strip().lower()

    def validate_password(self, value):
        """
        Additional password validation
        """
        if not value:
            raise serializers.ValidationError("Password is required.")
        
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        
        if len(value) > 128:
            raise serializers.ValidationError("Password cannot exceed 128 characters.")
        
        # Check for at least one letter
        if not re.search(r'[a-zA-Z]', value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        
        # Check for at least one number
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one number.")
        
        # Check for common weak passwords
        common_passwords = ['password', '12345678', 'qwerty', 'abc123', 'password123']
        if value.lower() in common_passwords:
            raise serializers.ValidationError("This password is too common. Please choose a stronger password.")
        
        return value

    def validate_first_name(self, value):
        """
        Validate first name if provided
        """
        if value and value.strip():
            # Check for valid characters (letters, spaces, hyphens, apostrophes)
            if not re.match(r"^[a-zA-Z\s\-']+$", value):
                raise serializers.ValidationError(
                    "First name can only contain letters, spaces, hyphens, and apostrophes."
                )
            if len(value.strip()) > 150:
                raise serializers.ValidationError("First name cannot exceed 150 characters.")
            return value.strip()
        return value

    def validate_last_name(self, value):
        """
        Validate last name if provided
        """
        if value and value.strip():
            # Check for valid characters (letters, spaces, hyphens, apostrophes)
            if not re.match(r"^[a-zA-Z\s\-']+$", value):
                raise serializers.ValidationError(
                    "Last name can only contain letters, spaces, hyphens, and apostrophes."
                )
            if len(value.strip()) > 150:
                raise serializers.ValidationError("Last name cannot exceed 150 characters.")
            return value.strip()
        return value

    def validate(self, attrs):
        """
        Validate password confirmation match
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password2": "Password confirmation does not match. Please ensure both passwords are identical."
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        # Create default preferences for new user
        UserPreferences.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login with validation
    """
    username = serializers.CharField(
        required=True,
        max_length=150,
        help_text="Your username"
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'},
        help_text="Your password"
    )

    def validate_username(self, value):
        """
        Validate username is not empty
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Username is required and cannot be empty.")
        
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters long.")
        
        return value.strip()

    def validate_password(self, value):
        """
        Validate password is not empty
        """
        if not value:
            raise serializers.ValidationError("Password is required and cannot be empty.")
        
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        
        return value

    def validate(self, attrs):
        """
        Validate user credentials
        """
        from django.contrib.auth import authenticate
        
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            
            if not user:
                raise serializers.ValidationError({
                    "non_field_errors": ["Invalid username or password. Please check your credentials and try again."]
                })
            
            if not user.is_active:
                raise serializers.ValidationError({
                    "non_field_errors": ["This account has been deactivated. Please contact support."]
                })
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError({
                "non_field_errors": ["Both username and password are required."]
            })


class UserSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'profile_image')
    
    def get_profile_image(self, obj):
        if hasattr(obj, 'preferences') and obj.preferences.profile_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.preferences.profile_image.url)
        return None


class UserProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'profile_image')
        read_only_fields = ('id', 'username', 'profile_image')
    
    def get_profile_image(self, obj):
        if hasattr(obj, 'preferences') and obj.preferences.profile_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.preferences.profile_image.url)
        return None


class UserPreferencesSerializer(serializers.ModelSerializer):
    profile_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = UserPreferences
        fields = ('dark_mode', 'default_priority', 'profile_image', 'profile_image_url')
        extra_kwargs = {
            'profile_image': {'write_only': True, 'required': False}
        }
    
    def get_profile_image_url(self, obj):
        if obj.profile_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
        return None

