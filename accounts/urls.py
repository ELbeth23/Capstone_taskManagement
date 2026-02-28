from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserProfileView, UserPreferencesView, DeleteAccountView, UploadProfileImageView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('preferences/', UserPreferencesView.as_view(), name='preferences'),
    path('upload-profile-image/', UploadProfileImageView.as_view(), name='upload_profile_image'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete_account'),
]
