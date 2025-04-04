from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.utils.dateparse import parse_datetime

def task_list(request):
    tasks = Task.objects.all()
    priority_filter = request.GET.get('priority', None)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        due_date = request.POST.get('due_date')
        title = request.POST['title']
        description = request.POST['description']
        priority = request.POST['priority']
        status = request.POST['status']
        due_date=parse_datetime(due_date) if due_date else None
       
        Task.objects.create(title=title, description=description, priority=priority, status=status)
        return redirect('task_list')
    return render(request, 'tasks/add_task.html')

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.title = request.POST['title']
        task.description = request.POST['description']
        task.priority = request.POST['priority']
        task.status = request.POST['status']
        due_date = request.POST.get('due_date')
        task.due_date = parse_datetime(due_date) if due_date else None
    
        task.save()
        return redirect('task_list')
    return render(request, 'tasks/edit_task.html', {'task': task})

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')

