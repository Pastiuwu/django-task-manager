from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from .models import Task
from datetime import datetime, timedelta

def task_list(request):
    query = request.GET.get('q')
    if query:
        tasks = Task.objects.filter(description__icontains=query)
    else:
        tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'tasks/index.html', {'tasks': tasks, 'query': query})


def add_task(request):
    if request.method == 'POST':
        description = request.POST['description']
        priority = request.POST['priority']
        deadline = request.POST.get('deadline')
        if deadline:
            deadline = timezone.make_aware(datetime.strptime(deadline.replace('T', ' '), '%Y-%m-%d %H:%M'))
        Task.objects.create(description=description, priority=priority, deadline=deadline)
        return redirect('task_list')
    return render(request, 'tasks/add_task.html')


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')


def toggle_task_completion(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')


def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.description = request.POST.get('description')
        task.priority = request.POST.get('priority')

        deadline_str = request.POST.get('deadline')
        if deadline_str:
            task.deadline = timezone.make_aware(datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M'))

        task.save()
        return redirect('task_list')

    return render(request, 'tasks/edit_task.html', {'task': task})


# NUEVAS VISTAS

def completed_tasks(request):
    tasks = Task.objects.filter(completed=True).order_by('-created_at')
    return render(request, 'tasks/completed_tasks.html', {'tasks': tasks})


def pending_tasks(request):
    tasks = Task.objects.filter(completed=False).order_by('deadline')
    return render(request, 'tasks/pending_tasks.html', {'tasks': tasks})


def approaching_tasks(request):
    now = timezone.now()
    soon = now + timedelta(days=3)
    tasks = Task.objects.filter(completed=False, deadline__range=(now, soon)).order_by('deadline')
    return render(request, 'tasks/approaching_tasks.html', {'tasks': tasks})


def overdue_tasks(request):
    now = timezone.now()
    tasks = Task.objects.filter(completed=False, deadline__lt=now).order_by('deadline')
    return render(request, 'tasks/overdue_tasks.html', {'tasks': tasks})
