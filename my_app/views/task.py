from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from ..models import Task
from ..serializers import TaskCreateSerializer, TaskDetailsSerializer


@api_view(['POST'])
def task_create(request: Request):
    serializer = TaskCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(assignee=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def task_get(request: Request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskDetailsSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def tasks_get(request: Request):
    task = Task.objects.all()
    if not task.exists():
        return Response({'error': 'Tasks not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskDetailsSerializer(task, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def tasks_stats(request: Request):
    stats = Task.objects.aggregate(
        total_tasks=Count('id'),
        new_tasks=Count('id', filter=Q(status=Task.Status.NEW)),
        in_progress_tasks=Count('id', filter=Q(status=Task.Status.IN_PROGRESS)),
        pending_tasks=Count('id', filter=Q(status=Task.Status.PENDING)),
        blocked_tasks=Count('id', filter=Q(status=Task.Status.BLOCKED)),
        done_tasks=Count('id', filter=Q(status=Task.Status.DONE)),
        overdue_date_tasks=Count('id', filter=Q(due_date__lt=timezone.now()) & ~Q(status=Task.Status.DONE))
    )
    if not stats:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    return Response(stats, status=status.HTTP_200_OK)
