from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('toggle/<int:task_id>/', views.toggle_task_completion, name='toggle_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('completadas/', views.completed_tasks, name='completed_tasks'),
    path('pendientes/', views.pending_tasks, name='pending_tasks'),
    path('proximas/', views.approaching_tasks, name='approaching_tasks'),
    path('vencidas/', views.overdue_tasks, name='overdue_tasks'),
]
