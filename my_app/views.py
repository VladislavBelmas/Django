from pickle import PUT

from django.db.models import Count, Q
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Task, Project, Tag
from .serialisers import TaskCreateSerializer, TaskDetailsSerializer, ProjectSerializer, TagsSerializer

def hello_name(request: Request, name):
    return HttpResponse(f"<h1>Hello, {name}</h1>")

def hello_world(request: Request):
    return HttpResponse(f"<h1>Hello world!</h1>")


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
    try:
        task = Task.objects.all()
    except Task.DoesNotExist:
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

@api_view(['GET'])
def projects_get(request: Request):
    projects = Project.objects.all()

    serializer = ProjectSerializer(projects, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def tags_get(request: Request):
    tags = Tag.objects.all()

    serializer = TagsSerializer(tags, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT'])
def tag_detail(request: Request, pk):
    try:
        tag = Tag.objects.get(pk=pk)
    except Tag.DoesNotExist:
        return Response({'error': 'Tag not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TagsSerializer(tag)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = TagsSerializer(tag, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def tag_post(request: Request):
    serializer = TagsSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def tag_delete(request: Request, pk):
    try:
        tag = Tag.objects.get(pk=pk)
    except Tag.DoesNotExist:
        return Response({'error': 'Tag not found'}, status=status.HTTP_404_NOT_FOUND)
    tag.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)