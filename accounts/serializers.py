from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserPreferences


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        # Create default preferences for new user
        UserPreferences.objects.create(user=user)
        return user


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

