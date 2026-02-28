from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home, register_page, login_page, dashboard_page, tasks_page, calendar_page, settings_page

urlpatterns = [
    path('', home, name='home'),
    path('register/', register_page, name='register_page'),
    path('login/', login_page, name='login_page'),
    path('dashboard/', dashboard_page, name='dashboard_page'),
    path('tasks/', tasks_page, name='tasks_page'),
    path('calendar/', calendar_page, name='calendar_page'),
    path('settings/', settings_page, name='settings_page'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/tasks/', include('tasks.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)