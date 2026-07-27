from django.contrib import admin
from .models import Category, Task, Subtask

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 3


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'status', 'deadline')
    search_fields = ('title', 'categories__name', 'status', 'deadline')
    list_filter = ('categories', 'status', 'deadline')
    ordering = ('deadline', 'created_at')
    fields = ('title', 'description', 'categories', 'status', 'deadline')
    list_per_page = 2


@admin.register(Subtask)
class SubtaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'task', 'status', 'deadline')
    search_fields = ('task__title', 'status', 'deadline')
    list_filter = ('task', 'status', 'deadline')
    ordering = ('deadline', 'created_at')
    fields = ('title', 'description', 'task', 'status', 'deadline')
    list_per_page = 2