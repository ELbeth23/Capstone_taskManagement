from django.urls import path
from .views import TaskListCreateView, TaskDetailView, TaskSummaryView, TaskAnalyticsView, TaskCalendarView

urlpatterns = [
    path('', TaskListCreateView.as_view(), name='task_list_create'),
    path('summary/', TaskSummaryView.as_view(), name='task_summary'),
    path('analytics/', TaskAnalyticsView.as_view(), name='task_analytics'),
    path('calendar/', TaskCalendarView.as_view(), name='task_calendar'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
]
