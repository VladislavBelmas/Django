from rest_framework import serializers
from .models import Task

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'due_date']

class TaskDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'