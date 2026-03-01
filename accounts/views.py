from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, UserProfileSerializer, UserPreferencesSerializer
from .models import UserPreferences


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': UserSerializer(user, context={'request': request}).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'error': 'Registration failed',
                'details': serializer.errors if hasattr(serializer, 'errors') else str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Custom login view with validation
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                },
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Login failed',
                'details': serializer.errors if hasattr(serializer, 'errors') else str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user
    
    def get_serializer_context(self):
        return {'request': self.request}


class UserPreferencesView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    def get(self, request):
        """Get user preferences"""
        preferences, created = UserPreferences.objects.get_or_create(user=request.user)
        serializer = UserPreferencesSerializer(preferences, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request):
        """Update user preferences"""
        preferences, created = UserPreferences.objects.get_or_create(user=request.user)
        serializer = UserPreferencesSerializer(preferences, data=request.data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Preferences updated successfully',
                'preferences': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadProfileImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        """Upload profile image"""
        if 'profile_image' not in request.FILES:
            return Response({'error': 'No image file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        preferences, created = UserPreferences.objects.get_or_create(user=request.user)
        
        # Delete old image if exists
        if preferences.profile_image:
            preferences.profile_image.delete(save=False)
        
        preferences.profile_image = request.FILES['profile_image']
        preferences.save()
        
        image_url = request.build_absolute_uri(preferences.profile_image.url)
        
        return Response({
            'message': 'Profile image uploaded successfully',
            'profile_image_url': image_url
        }, status=status.HTTP_200_OK)
    
    def delete(self, request):
        """Delete profile image"""
        try:
            preferences = UserPreferences.objects.get(user=request.user)
            if preferences.profile_image:
                preferences.profile_image.delete(save=True)
                return Response({'message': 'Profile image deleted successfully'})
            return Response({'error': 'No profile image to delete'}, status=status.HTTP_404_NOT_FOUND)
        except UserPreferences.DoesNotExist:
            return Response({'error': 'User preferences not found'}, status=status.HTTP_404_NOT_FOUND)


class DeleteAccountView(APIView):
    
    def delete(self, request):
        """Delete user account and all associated data"""
        user = request.user
        username = user.username
        
        # Delete user (this will cascade delete tasks and preferences)
        user.delete()
        
        return Response({
            'message': f'Account {username} has been permanently deleted'
        }, status=status.HTTP_200_OK)
