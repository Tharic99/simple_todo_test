from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json  # Import json module here
from .models import TodoItem, Status
from .forms import TodoItemForm, UserRegisterForm

@login_required
def todo_list(request):
    # Default sorting fields
    default_sort_by = 'status__name'
    default_order = 'asc'

    # Retrieve sorting parameters from request
    sort_by = request.GET.get('sort_by', default_sort_by)
    order = request.GET.get('order', default_order)

    # Map sort_by to correct field names
    if sort_by == 'category__name':
        sort_field = 'category__name'
    elif sort_by == 'title':
        sort_field = 'title'
    elif sort_by == 'description':
        sort_field = 'description'
    elif sort_by == 'due_date':
        sort_field = 'due_date'
    elif sort_by == 'status__name':
        sort_field = 'status__name'
    else:
        sort_field = default_sort_by

    # Apply descending order if specified
    if order == 'desc':
        sort_field = '-' + sort_field

    # Query with sorting
    todo_items = TodoItem.objects.all().order_by(sort_field)

    context = {
        'todo_items': todo_items,
        'current_sort_by': sort_by,
        'current_order': order
    }
    
    return render(request, 'todo/todo_list.html', context)

@login_required
def edit_todo(request, pk):
    todo_item = get_object_or_404(TodoItem, pk=pk)

    if request.method == 'POST':
        if 'save' in request.POST:
            form = TodoItemForm(request.POST, instance=todo_item)
            if form.is_valid():
                form.save()
                return redirect('todo:todo_list')
        elif 'delete' in request.POST:
            return redirect('todo:confirm_delete', pk=pk)
    else:
        form = TodoItemForm(instance=todo_item)
    
    return render(request, 'todo/edit_todo.html', {'form': form, 'todo_item': todo_item})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('todo_list')
    else:
        form = UserRegisterForm()
    return render(request, 'todo/register.html', {'form': form})

@login_required
def add_todo(request):
    if request.method == 'POST':
        form = TodoItemForm(request.POST)
        if form.is_valid():
            todo_item = form.save(commit=False)
            todo_item.user = request.user  # Set the user field
            todo_item.save()
            return redirect('todo:todo_list')
    else:
        form = TodoItemForm()

    return render(request, 'todo/add_todo.html', {'form': form})

@login_required
def confirm_delete(request, pk):
    todo_item = get_object_or_404(TodoItem, pk=pk)
    if request.method == 'POST':
        todo_item.delete()
        return redirect('todo:todo_list')  # Redirect to the list view after deletion
    return render(request, 'todo/confirm_delete.html', {'todo_item': todo_item})

@login_required
def update_task_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            task_id = data.get('id')
            status_name = data.get('status')
            status = Status.objects.get(name=status_name)
            task = TodoItem.objects.get(id=task_id)
            task.status = status
            task.save()
            return JsonResponse({'status': 'success'})
        except (Status.DoesNotExist, TodoItem.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Task or status not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
