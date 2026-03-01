from rest_framework import generics, status
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
    
    def create(self, request, *args, **kwargs):
        """
        Override create to provide better error handling
        """
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({
                'message': 'Task created successfully',
                'task': serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({
                'error': 'Failed to create task',
                'details': serializer.errors if hasattr(serializer, 'errors') else str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        """
        Override update to provide better error handling
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            return Response({
                'message': 'Task updated successfully',
                'task': serializer.data
            })
        except Exception as e:
            return Response({
                'error': 'Failed to update task',
                'details': serializer.errors if hasattr(serializer, 'errors') else str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class TaskSummaryView(generics.GenericAPIView):

    def get(self, request):
        from datetime import datetime, timedelta
        
        tasks = Task.objects.filter(user=request.user)
        
        # Get filter parameters
        period = request.query_params.get('period', 'total')  # total, week, month
        year = request.query_params.get('year')
        week = request.query_params.get('week')
        month = request.query_params.get('month')

        total = tasks.count()
        completed = tasks.filter(status='completed').count()
        pending = tasks.filter(status='pending').count()
        overdue = tasks.filter(
            due_date__lt=timezone.now(),
            status='pending'
        ).count()
        
        # Calculate completion rate based on period
        if period == 'week' and year and week:
            # Get tasks for specific week using ISO 8601 week date
            year = int(year)
            week = int(week)
            
            # Use ISO calendar to get the correct week start
            # Find the Monday of the given ISO week
            jan_4 = datetime(year, 1, 4)  # Jan 4 is always in week 1
            week_1_start = jan_4 - timedelta(days=jan_4.weekday())  # Monday of week 1
            start_of_week = week_1_start + timedelta(weeks=week-1)
            end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)
            
            # Make timezone aware
            start_of_week = timezone.make_aware(start_of_week) if timezone.is_naive(start_of_week) else start_of_week
            end_of_week = timezone.make_aware(end_of_week) if timezone.is_naive(end_of_week) else end_of_week
            
            # Only count tasks with due dates in this week that have passed
            now = timezone.now()
            end_date = min(end_of_week, now)
            
            # Filter tasks for this week - only tasks with due dates that have passed
            tasks_in_period = tasks.filter(
                due_date__isnull=False,
                due_date__gte=start_of_week,
                due_date__lte=end_date
            )
            
            period_label = f"Week {week}"
            date_range = f"{start_of_week.strftime('%b %d')} - {end_of_week.strftime('%b %d, %Y')}"
            
        elif period == 'month' and year and month:
            # Get tasks for specific month
            year = int(year)
            month = int(month)
            
            start_of_month = datetime(year, month, 1)
            if month == 12:
                end_of_month = datetime(year + 1, 1, 1) - timedelta(seconds=1)
            else:
                end_of_month = datetime(year, month + 1, 1) - timedelta(seconds=1)
            
            # Make timezone aware
            start_of_month = timezone.make_aware(start_of_month) if timezone.is_naive(start_of_month) else start_of_month
            end_of_month = timezone.make_aware(end_of_month) if timezone.is_naive(end_of_month) else end_of_month
            
            # Only count tasks with due dates in this month that have passed
            now = timezone.now()
            end_date = min(end_of_month, now)
            
            # Filter tasks for this month - only tasks with due dates that have passed
            tasks_in_period = tasks.filter(
                due_date__isnull=False,
                due_date__gte=start_of_month,
                due_date__lte=end_date
            )
            
            month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                          'July', 'August', 'September', 'October', 'November', 'December']
            period_label = f"{month_names[month-1]} {year}"
            date_range = f"{start_of_month.strftime('%b %d')} - {end_of_month.strftime('%b %d, %Y')}"
            
        else:
            # Total (all time) - tasks that have reached their due date
            tasks_in_period = tasks.filter(
                due_date__isnull=False,
                due_date__lte=timezone.now()
            )
            period_label = "All Time"
            date_range = "Total completion rate"
        
        # Calculate completion rate for the period
        total_due = tasks_in_period.count()
        completed_due = tasks_in_period.filter(status='completed').count()
        pending_due = tasks_in_period.filter(status='pending').count()
        
        completion_rate = 0
        if total_due > 0:
            completion_rate = round((completed_due / total_due) * 100, 1)

        return Response({
            "total_tasks": total,
            "completed_tasks": completed,
            "pending_tasks": pending,
            "overdue_tasks": overdue,
            "completion_rate": completion_rate,
            "tasks_due": total_due,
            "completed_due": completed_due,
            "pending_due": pending_due,
            "period": period,
            "period_label": period_label,
            "date_range": date_range
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
