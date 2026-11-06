from django.contrib.admin.templatetags.admin_list import paginator_number
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from ..models import Task, SubTask
from ..serializers import SubTaskCreateSerializer, SubTaskSerializer


# @api_view(['POST'])
# def subtask_post(request: Request, task_pk):
#     try:
#         task = Task.objects.get(pk=task_pk)
#     except Task.DoesNotExist:
#         return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
#
#     serializer = SubTaskCreateSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         serializer.save(task=task)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

class SubTaskPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 5


class SubTaskListCreateView(APIView):
    pagination_class = SubTaskPagination

    def get(self, request: Request):
        queryset = SubTask.objects.all().order_by('-created_at')

        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        task_filter = request.query_params.get('task')
        if task_filter:
            queryset = queryset.filter(task_id=task_filter)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = SubTaskSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request: Request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):
    def get(self, request: Request, task_pk, pk):
        try:
            subtask = SubTask.objects.get(pk=pk, task_id=task_pk)
        except SubTask.DoesNotExist:
            return Response({'error': 'Subtask not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, task_pk, pk):
        try:
            subtask = SubTask.objects.get(pk=pk, task_id=task_pk)
        except SubTask.DoesNotExist:
            return Response({'error': 'Subtask not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubTaskSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, task_pk, pk):
        try:
            subtask = SubTask.objects.get(pk=pk, task_id=task_pk)
        except SubTask.DoesNotExist:
            return Response({'error': 'Subtask not found'}, status=status.HTTP_404_NOT_FOUND)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)