
from django.db import models
from django.conf import settings

class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)


class ProjectFile(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False)
    file = models.FileField(upload_to='projects')
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'task_manager_project_file'
        verbose_name = 'project file'
        verbose_name_plural = 'project files'

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='')
    description = models.TextField(null=False, blank=False)
    files = models.ManyToManyField(ProjectFile, related_name='projects', blank=True)
    created_at = models.DateField(auto_now_add=True)

    @property
    def count_of_files(self):
        return self.files.count()


    class Meta:
        db_table = 'task_manager_project'
        ordering = ['-name']
        verbose_name = 'project'
        verbose_name_plural = 'projects'
        constraints = (models.UniqueConstraint(
            fields=('name', 'description'),
            name='unique_project_title_description'
        ),)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Task(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        IN_PROGRESS = "in_progress", "In progress"
        PENDING = "pending", "Pending"
        BLOCKED = "blocked", "Blocked"
        DONE = "done", "Done"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    title = models.CharField(max_length=100, unique_for_date='due_date', help_text='Название задачи', unique=True)
    description = models.TextField(blank=True, null=True, help_text='Описание задачи')
    categories = models.ManyToManyField(Category, blank=True, related_name='tasks', help_text='Категории задачи')
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.NEW, help_text='Статус задачи')
    priority = models.CharField(max_length=15, choices=Priority.choices, default=Priority.MEDIUM)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks',
                                verbose_name='', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at', help_text='Дата и время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at', help_text='Дата и время создания')
    tags = models.ManyToManyField(Tag, related_name='tasks', blank=True)
    due_date = models.DateTimeField(help_text='Дата и время дедлайнa')
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name='tasks')

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-due_date', 'assignee']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        constraints = (models.UniqueConstraint(
            fields=('title', 'project'),
            name='unique_task_title_project'
        ),)


    def __str__(self):
        return self.title


class Subtask(models.Model):
    title = models.CharField(max_length=100, unique_for_date='due_date', help_text='Название подзадачи', unique=True)
    description = models.TextField(blank=True, null=True, help_text='Описание подзадачи')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, help_text='Основная задача')
    status = models.CharField(max_length=20, choices=Task.Status.choices,
                              default=Task.Status.NEW, help_text='Статус задачи')
    due_date = models.DateTimeField(help_text='Дата и время дедлайнa')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at', help_text='Дата и время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at', help_text='Дата и время создания')

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'Subtask'
        verbose_name_plural = 'Subtasks'

    def __str__(self):
        return f"{self.title} (Подзадача для: {self.task.title})"




