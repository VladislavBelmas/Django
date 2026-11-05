from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from ..models import Task, Subtask
from ..serializers import SubTaskCreateSerializer, SubtaskSerializer


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


class SubTaskListCreateView(APIView):
    def get(self, request):
        subtasks = Subtask.objects.all()
        serializer = SubtaskSerializer(subtasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):
    def get(self, request, task_pk, pk):
        try:
            subtask = Subtask.objects.get(pk=pk, task_id=task_pk)
        except Subtask.DoesNotExist:
            return Response({'error': 'Subtask not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubtaskSerializer(subtask)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, task_pk, pk):
        try:
            subtask = Subtask.objects.get(pk=pk, task_id=task_pk)
        except Subtask.DoesNotExist:
            return Response({'error': 'Subtask not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubtaskSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_pk, pk):
        try:
            subtask = Subtask.objects.get(pk=pk, task_id=task_pk)
        except Subtask.DoesNotExist:
            return Response({'error': 'Subtask not found'}, status=status.HTTP_404_NOT_FOUND)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)