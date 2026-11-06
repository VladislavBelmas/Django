from django.db.models import Count, Q
from django.db.models.functions import ExtractWeekDay
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
    week_day = request.query_params.get('week_day')
    tasks = Task.objects.all()

    if week_day:
        try:
            week_day = int(week_day)
            tasks = tasks.annotate(week_day=ExtractWeekDay('due_date')).filter(week_day=week_day)
        except ValueError:
            return Response({'error': 'Week day must be a number (1-7, 1-Sunday)'},
                            status=status.HTTP_400_BAD_REQUEST
                            )
    if not tasks.exists():
        return Response({'error': 'Tasks not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskDetailsSerializer(tasks, many=True)
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
