# settings/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from todo.models import Category, Status  # Import from the 'todo' app
from .forms import CategoryForm, StatusForm

@login_required
def settings_home(request):
    """Default page for settings."""
    return render(request, 'settings/settings_home.html')

@login_required
def manage_categories(request):
    """Manage categories including default status."""
    categories = Category.objects.all()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('is_default'):
                Category.objects.filter(is_default=True).update(is_default=False)
            form.save()
            return redirect('settings:manage_categories')
    else:
        form = CategoryForm()
    
    return render(request, 'settings/manage_categories.html', {'categories': categories, 'form': form})

@login_required
def manage_statuses(request):
    """Manage statuses including default status."""
    statuses = Status.objects.all()
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('is_default'):
                Status.objects.filter(is_default=True).update(is_default=False)
            form.save()
            return redirect('settings:manage_statuses')
    else:
        form = StatusForm()
    
    return render(request, 'settings/manage_statuses.html', {'statuses': statuses, 'form': form})
