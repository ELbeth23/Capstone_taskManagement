from rest_framework import generics
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwner


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)

        # Filter by status
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Filter by priority
        priority = self.request.query_params.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)

        # Filter by due date
        due_date = self.request.query_params.get('due_date')
        if due_date:
            queryset = queryset.filter(due_date__date=due_date)

        # Filter overdue tasks
        overdue = self.request.query_params.get('overdue')
        if overdue == 'true':
            queryset = queryset.filter(due_date__lt=timezone.now(), status='pending')

        # Filter upcoming tasks (next 7 days)
        upcoming = self.request.query_params.get('upcoming')
        if upcoming == 'true':
            today = timezone.now()
            next_week = today + timedelta(days=7)
            queryset = queryset.filter(due_date__gte=today, due_date__lte=next_week, status='pending')

        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskSummaryView(generics.GenericAPIView):

    def get(self, request):
        tasks = Task.objects.filter(user=request.user)

        total = tasks.count()
        completed = tasks.filter(status='completed').count()
        pending = tasks.filter(status='pending').count()
        overdue = tasks.filter(
            due_date__lt=timezone.now(),
            status='pending'
        ).count()

        return Response({
            "total_tasks": total,
            "completed_tasks": completed,
            "pending_tasks": pending,
            "overdue_tasks": overdue
        })


class TaskAnalyticsView(generics.GenericAPIView):
    def get(self, request):
        tasks = Task.objects.filter(user=request.user)

        # Weekly performance (last 7 days)
        today = timezone.now().date()
        weekly_data = []
        for i in range(6, -1, -1):
            date = today - timedelta(days=i)
            completed = tasks.filter(
                status='completed',
                updated_at__date=date
            ).count()
            created = tasks.filter(created_at__date=date).count()
            weekly_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'completed': completed,
                'created': created
            })

        # Priority distribution
        priority_dist = {
            'high': tasks.filter(priority='high').count(),
            'medium': tasks.filter(priority='medium').count(),
            'low': tasks.filter(priority='low').count()
        }

        # Status distribution
        status_dist = {
            'completed': tasks.filter(status='completed').count(),
            'pending': tasks.filter(status='pending').count()
        }

        # Completion rate (last 30 days)
        thirty_days_ago = today - timedelta(days=30)
        recent_tasks = tasks.filter(created_at__date__gte=thirty_days_ago)
        total_recent = recent_tasks.count()
        completed_recent = recent_tasks.filter(status='completed').count()
        completion_rate = (completed_recent / total_recent * 100) if total_recent > 0 else 0

        # Productivity score (0-100)
        overdue = tasks.filter(due_date__lt=timezone.now(), status='pending').count()
        total = tasks.count()
        productivity_score = max(0, 100 - (overdue * 10)) if total > 0 else 0

        return Response({
            'weekly_performance': weekly_data,
            'priority_distribution': priority_dist,
            'status_distribution': status_dist,
            'completion_rate': round(completion_rate, 1),
            'productivity_score': min(100, productivity_score)
        })


class TaskCalendarView(generics.GenericAPIView):
    def get(self, request):
        # Get year and month from query params, default to current
        year = int(request.query_params.get('year', timezone.now().year))
        month = int(request.query_params.get('month', timezone.now().month))

        # Get first and last day of the month
        first_day = datetime(year, month, 1)
        if month == 12:
            last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = datetime(year, month + 1, 1) - timedelta(days=1)

        # Get all tasks for the user in this month
        tasks = Task.objects.filter(
            user=request.user,
            due_date__gte=first_day,
            due_date__lte=last_day
        ).order_by('due_date')

        # Group tasks by date
        tasks_by_date = {}
        for task in tasks:
            date_key = task.due_date.strftime('%Y-%m-%d')
            if date_key not in tasks_by_date:
                tasks_by_date[date_key] = []

            tasks_by_date[date_key].append({
                'id': task.id,
                'title': task.title,
                'priority': task.priority,
                'status': task.status,
                'due_date': task.due_date.isoformat()
            })

        return Response({
            'year': year,
            'month': month,
            'tasks_by_date': tasks_by_date
        })



class TaskAnalyticsView(generics.GenericAPIView):
    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        
        # Weekly performance (last 7 days)
        today = timezone.now().date()
        weekly_data = []
        for i in range(6, -1, -1):
            date = today - timedelta(days=i)
            completed = tasks.filter(
                status='completed',
                updated_at__date=date
            ).count()
            created = tasks.filter(created_at__date=date).count()
            weekly_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'completed': completed,
                'created': created
            })
        
        # Priority distribution
        priority_dist = {
            'high': tasks.filter(priority='high').count(),
            'medium': tasks.filter(priority='medium').count(),
            'low': tasks.filter(priority='low').count()
        }
        
        # Status distribution
        status_dist = {
            'completed': tasks.filter(status='completed').count(),
            'pending': tasks.filter(status='pending').count()
        }
        
        # Completion rate (last 30 days)
        thirty_days_ago = today - timedelta(days=30)
        recent_tasks = tasks.filter(created_at__date__gte=thirty_days_ago)
        total_recent = recent_tasks.count()
        completed_recent = recent_tasks.filter(status='completed').count()
        completion_rate = (completed_recent / total_recent * 100) if total_recent > 0 else 0
        
        # Productivity score (0-100)
        overdue = tasks.filter(due_date__lt=timezone.now(), status='pending').count()
        total = tasks.count()
        productivity_score = max(0, 100 - (overdue * 10)) if total > 0 else 0
        
        return Response({
            'weekly_performance': weekly_data,
            'priority_distribution': priority_dist,
            'status_distribution': status_dist,
            'completion_rate': round(completion_rate, 1),
            'productivity_score': min(100, productivity_score)
        })


class TaskCalendarView(generics.GenericAPIView):
    def get(self, request):
        # Get year and month from query params, default to current
        year = int(request.query_params.get('year', timezone.now().year))
        month = int(request.query_params.get('month', timezone.now().month))
        
        # Get first and last day of the month
        first_day = datetime(year, month, 1)
        if month == 12:
            last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = datetime(year, month + 1, 1) - timedelta(days=1)
        
        # Get all tasks for the user in this month
        tasks = Task.objects.filter(
            user=request.user,
            due_date__gte=first_day,
            due_date__lte=last_day
        ).order_by('due_date')
        
        # Group tasks by date
        tasks_by_date = {}
        for task in tasks:
            date_key = task.due_date.strftime('%Y-%m-%d')
            if date_key not in tasks_by_date:
                tasks_by_date[date_key] = []
            
            tasks_by_date[date_key].append({
                'id': task.id,
                'title': task.title,
                'priority': task.priority,
                'status': task.status,
                'due_date': task.due_date.isoformat()
            })
        
        return Response({
            'year': year,
            'month': month,
            'tasks_by_date': tasks_by_date
        })


class DailySummaryView(generics.GenericAPIView):
    def get(self, request):
        """Get daily summary data for dashboard display"""
        tasks = Task.objects.filter(user=request.user)
        
        # Get today's date
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)
        
        # Tasks due today
        tasks_today = tasks.filter(
            due_date__date=today,
            status='pending'
        ).values('id', 'title', 'priority', 'due_date')
        
        # Tasks due tomorrow
        tasks_tomorrow = tasks.filter(
            due_date__date=tomorrow,
            status='pending'
        ).values('id', 'title', 'priority', 'due_date')
        
        # Overdue tasks
        overdue_tasks = tasks.filter(
            due_date__lt=timezone.now(),
            status='pending'
        ).values('id', 'title', 'priority', 'due_date')
        
        # Tasks completed today
        completed_today = tasks.filter(
            updated_at__date=today,
            status='completed'
        ).count()
        
        # Total pending tasks
        total_pending = tasks.filter(status='pending').count()
        
        return Response({
            'date': today.strftime('%B %d, %Y'),
            'summary': {
                'completed_today': completed_today,
                'tasks_due_today': tasks_today.count(),
                'tasks_due_tomorrow': tasks_tomorrow.count(),
                'overdue_tasks': overdue_tasks.count(),
                'total_pending': total_pending
            },
            'tasks_today': list(tasks_today),
            'tasks_tomorrow': list(tasks_tomorrow),
            'overdue_tasks': list(overdue_tasks[:5])  # Limit to 5
        })
