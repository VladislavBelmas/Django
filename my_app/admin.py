from django.contrib import admin, messages
from django.db.models import Value
from django.db.models.functions import Replace
from django.template.defaultfilters import truncatechars
from django.utils import timezone

from .models import Category, Task, Subtask, Project, Tag, ProjectFile


@admin.action(description='Spaces to underscores')
def spaces_underscores(modeladmin, request, queryset):
    queryset.update(name=Replace('name', Value(' '), Value('_')), updated_at=timezone.now())


@admin.action(description='Closing every tasks')
def status_close(modeladmin, request, queryset):
    updated_count = queryset.update(status=Task.Status.DONE, updated_at=timezone.now())
    modeladmin.message_user(request, f"Статус всех выделенных задач успешно обновлен на 'Закрыто'. "
                            f"Количество обновленных задач: {updated_count}.", messages.SUCCESS)


@admin.action(description='Set priority to low')
def priority_update_low(modeladmin, request, queryset):
    queryset.update(priority=Task.Priority.LOW, updated_at=timezone.now())


@admin.action(description='Set priority to medium')
def priority_update_medium(modeladmin, request, queryset):
    queryset.update(priority=Task.Priority.MEDIUM, updated_at=timezone.now())


@admin.action(description='Set priority to high')
def priority_update_high(modeladmin, request, queryset):
    queryset.update(priority=Task.Priority.HIGH, updated_at=timezone.now())


class SubTaskInLine(admin.StackedInline):
    model = Subtask
    extra = 1



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 3


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'project', 'status', 'priority', 'created_at', 'updated_at', 'due_date', 'assignee')
    search_fields = ('title', 'categories__name')
    list_filter = ('status', 'priority', 'project', 'created_at', 'due_date', 'assignee')
    ordering = ('due_date', 'created_at')
    fields = ('title', 'description', 'categories', 'status', 'due_date')
    list_per_page = 2

    inlines = (SubTaskInLine,)

    actions = (status_close,
               priority_update_low,
               priority_update_medium,
               priority_update_high,)

    @admin.display(description='title', ordering='title')
    def short_title(self, obj):
        return truncatechars(obj.title, 10)


@admin.register(Subtask)
class SubtaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'task', 'status', 'due_date')
    search_fields = ('task__title', 'status', 'due_date')
    list_filter = ('task', 'status', 'due_date')
    ordering = ('due_date', 'created_at')
    fields = ('title', 'description', 'task', 'status', 'due_date')
    list_per_page = 2

    actions = (status_close,)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_count_of_files', 'created_at')
    search_fields = ('name',)
    ordering = ('-name',)

    actions = (spaces_underscores,)

    def display_count_of_files(self, obj):
        return obj.count_of_files

    display_count_of_files.short_description = 'count of files'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'file', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)
