from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Task


def index(request):
    tasks = Task.objects.all()
    return render(request, 'index.html', {'tasks': tasks})

@csrf_exempt
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        status = request.POST.get('status')
        Task.objects.create(title=title, description=description, priority=priority, status=status)
        return JsonResponse({'message': 'Task added successfully!'})
    return render(request, 'add_task.html')

@csrf_exempt
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.title = request.POST.get('title', task.title)
        task.description = request.POST.get('description', task.description)
        task.priority = request.POST.get('priority', task.priority)
        task.status = request.POST.get('status', task.status)
        task.save()
        return JsonResponse({'message': 'Task updated successfully!'})
    return render(request, 'edit_task.html', {'task': task})


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return JsonResponse({'message': 'Task deleted successfully!'})


def view_all_tasks(request):
    tasks = Task.objects.all()
    return render(request, 'view_tasks.html', {'tasks': tasks})


def filter_tasks_by_priority(request, priority):
    tasks = Task.objects.filter(priority=priority)
    return render(request, 'view_tasks.html', {'tasks': tasks})
