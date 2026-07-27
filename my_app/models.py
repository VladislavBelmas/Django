from django.db import models

STATUS_CHOICES = [
    ("NEW", "New"),
    ("IN_PROGRESS", "In progress"),
    ("PENDING", "Pending"),
    ("BLOCKED", "Blocked"),
    ("DONE", "Done"),
]


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=100, unique_for_date='deadline', help_text='Название задачи', unique=True)
    description = models.TextField(blank=True, null=True, help_text='Описание задачи')
    categories = models.ManyToManyField(Category, blank=True, related_name='tasks', help_text='Категории задачи')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW', help_text='Статус задачи')
    deadline = models.DateTimeField(help_text='Дата и время дедлайнa')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at', help_text='Дата и время создания')

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.title


class Subtask(models.Model):

    title = models.CharField(max_length=100, unique_for_date='deadline', help_text='Название подзадачи', unique=True)
    description = models.TextField(blank=True, null=True, help_text='Описание подзадачи')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, help_text='Основная задача')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW', help_text='Статус задачи')
    deadline = models.DateTimeField(help_text='Дата и время дедлайнa')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at', help_text='Дата и время создания')

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'Subtask'
        verbose_name_plural = 'Subtasks'

    def __str__(self):
        return f"{self.title} (Подзадача для: {self.task.title})"

