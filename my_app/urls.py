from django.urls import path
from . import views

urlpatterns = [
    path('hello/<str:name>', views.hello_name, name='hello_name'),
    path('hello/', views.hello_world, name='hello_world'),
    path('task/create', views.task_create, name='task_create'),
    path('task/<int:pk>', views.task_get, name='task_get'),
    path('task/', views.tasks_get, name='tasks_get'),
    path('task/stats', views.tasks_stats, name='tasks_stats')

]


