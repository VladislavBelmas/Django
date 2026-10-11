from datetime import timedelta
from os import environ
from django import setup
from django.utils import timezone

environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
setup()

from my_app.models import Task, Subtask

Task.objects.filter(title="Prepare presentation").delete()

new_task = Task.objects.create(title="Prepare presentation",
                               description="Prepare materials and slides for the presentation",
                               status="New",
                               due_date=(timezone.now() + timedelta(days=2)))

sub_task1 = Subtask.objects.create(title="Gather information",
                                   description="Find necessary information for the presentation",
                                   status="New",
                                   due_date=(timezone.now() + timedelta(days=2)),
                                   task=new_task)


sub_task2 = Subtask.objects.create(title="Create slides",
                                   description="Create presentation slides",
                                   status="New",
                                   due_date=(timezone.now() + timedelta(days=1)),
                                   task=new_task)



task_new_status = Task.objects.filter(status__iexact='New')
subtask_late_done = Subtask.objects.filter(status__iexact='Done', due_date__gt=timezone.now())

new_task.status = "In progress"
new_task.save()

sub_task1.due_date = timezone.now() - timedelta(days=2)
sub_task1.save()

sub_task2.description = "Create and format presentation slides"
sub_task2.save()

Task.objects.filter(title="Prepare presentation").delete()