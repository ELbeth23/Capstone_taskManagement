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
