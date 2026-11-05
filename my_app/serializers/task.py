from django.utils import timezone
from rest_framework import serializers
from ..models import Task
from .subtask import SubtaskSerializer


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date']

    def validate_due_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('Can not be in past')
        return value


class TaskDetailsSerializer(serializers.ModelSerializer):
    subtasks = SubtaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
