from django.contrib import admin
from django.urls import path, include
from .views import home, register_page, login_page

urlpatterns = [
    path('', home, name='home'),
    path('register/', register_page, name='register_page'),
    path('login/', login_page, name='login_page'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
]