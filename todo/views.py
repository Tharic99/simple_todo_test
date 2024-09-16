from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Case, When, IntegerField
import json
from .models import TodoItem, Status, Category
from .forms import TodoItemForm, UserRegisterForm, CategoryForm, StatusForm

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

    # Sort tasks with "Completed" status at the bottom, then by the specified field
    todo_items = TodoItem.objects.all().annotate(
        # Annotate each item with a flag: 0 if not "Completed", 1 if "Completed"
        completed_flag=Case(
            When(status__name='Completed', then=1),
            default=0,
            output_field=IntegerField()
        )
    ).order_by('completed_flag', sort_field)

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
            return redirect('todo:todo_list')
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
        # Check for a default category and set it as initial value
        try:
            default_category = Category.objects.get(is_default=True)
            form.fields['category'].initial = default_category
        except Category.DoesNotExist:
            pass

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

@login_required
def add_or_edit_category(request, pk=None):
    """Handle adding or editing categories, enforcing a single default."""
    if pk:
        category = get_object_or_404(Category, pk=pk)
    else:
        category = None

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            # Check if this category is being set as default
            if form.cleaned_data.get('is_default'):
                # Unset the current default category
                Category.objects.filter(is_default=True).update(is_default=False)
            form.save()
            return redirect('todo:category_list')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'todo/category_form.html', {'form': form})

@login_required
def add_or_edit_status(request, pk=None):
    """Handle adding or editing statuses, enforcing a single default."""
    if pk:
        status = get_object_or_404(Status, pk=pk)
    else:
        status = None

    if request.method == 'POST':
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            # Check if this status is being set as default
            if form.cleaned_data.get('is_default'):
                # Unset the current default status
                Status.objects.filter(is_default=True).update(is_default=False)
            form.save()
            return redirect('todo:status_list')
    else:
        form = StatusForm(instance=status)

    return render(request, 'todo/status_form.html', {'form': form})
