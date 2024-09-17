import contextlib
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import JsonResponse
from django.db.models import Case, When, IntegerField
from django.utils import timezone
import json
from .models import TodoItem, Status, Category
from settings.models import UserProfile  # Ensure this import is correct
from .forms import TodoItemForm, UserRegisterForm, CategoryForm, StatusForm

@login_required
def todo_list(request):
    default_sort_by = 'status__name'
    default_order = 'asc'

    # Retrieve sorting parameters from request
    sort_by = request.GET.get('sort_by', default_sort_by)
    order = request.GET.get('order', default_order)

    sort_field = {
        'category__name': 'category__name',
        'description': 'description',
        'due_date': 'due_date',
        'status__name': 'status__name',
        'title': 'title'
    }.get(sort_by, default_sort_by)

    # Apply descending order if specified
    sort_field = f'-{sort_field}' if order == 'desc' else sort_field

    # Sort tasks with "Completed" status at the bottom, then by the specified field
    todo_items = TodoItem.objects.all().annotate(
        completed_flag=Case(
            When(status__name='Completed', then=1),
            default=0,
            output_field=IntegerField()
        )
    ).order_by('completed_flag', sort_field)

    # Get the current user's profile
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    # Retrieve the 'show_completed' and 'enable_confirmations' values from the user's profile
    show_completed = 'yes' if user_profile.show_completed else 'no'
    enable_confirmations = user_profile.enable_confirmations  # This was missing before

    context = {
        'todo_items': todo_items,
        'current_sort_by': sort_by,
        'current_order': order,
        'show_completed': show_completed,
        'enable_confirmations': enable_confirmations,  # Pass the 'enable_confirmations' setting to the template
        'today': timezone.now().date()  # Pass the current date to the template
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

            # Handle the "Save and Add Another" button
            if 'add_another' in request.POST:
                return redirect('todo:add_todo')
            return redirect('todo:todo_list')
    else:
        form = TodoItemForm()

        # Check for a default category and set it as initial value
        with contextlib.suppress(Category.DoesNotExist):
            default_category = Category.objects.get(is_default=True)
            form.fields['category'].initial = default_category

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
    category = get_object_or_404(Category, pk=pk) if pk else None
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            # Check if this category is being set as default
            if form.cleaned_data.get('is_default'):
                Category.objects.filter(is_default=True).update(is_default=False)
            form.save()
            return redirect('todo:category_list')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'todo/category_form.html', {'form': form})


@login_required
def add_or_edit_status(request, pk=None):
    """Handle adding or editing statuses, enforcing a single default."""
    status = get_object_or_404(Status, pk=pk) if pk else None
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            # Check if this status is being set as default
            if form.cleaned_data.get('is_default'):
                Status.objects.filter(is_default=True).update(is_default=False)
            form.save()
            return redirect('todo:status_list')
    else:
        form = StatusForm(instance=status)

    return render(request, 'todo/status_form.html', {'form': form})


@login_required
def todo_by_categories(request):
    """Display to-do items grouped by categories."""
    categories = Category.objects.all()
    todos_by_category = {category: category.todos.all() for category in categories}
    return render(request, 'todo/todo_by_categories.html', {'todos_by_category': todos_by_category})


@login_required
def todo_by_status(request):
    """Display to-do items grouped by status with completed items always included."""
    statuses = Status.objects.all()
    todos_by_status = {}

    for status in statuses:
        todos = status.todos.all()  # Include all todos, regardless of their completion status
        todos_by_status[status] = todos

    return render(request, 'todo/todo_by_status.html', {
        'todos_by_status': todos_by_status,
    })
