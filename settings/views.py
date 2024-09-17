from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from todo.models import Category, Status
from .forms import CategoryForm, StatusForm
from .models import UserProfile
from django.views.decorators.csrf import csrf_exempt

@login_required
def settings_home(request):
    """Default page for settings with user info and general settings."""
    
    if request.method == 'POST':
        # Handle form submission for updating settings
        theme_mode = request.POST.get('theme_mode', 'auto')
        show_completed = request.POST.get('show_completed', 'no')

        # Save user profile settings
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile.theme_preference = theme_mode
        user_profile.show_completed = (show_completed == 'yes')
        user_profile.save()

        return redirect('settings:settings_home')

    # Retrieve current user settings
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    current_theme_mode = user_profile.theme_preference or 'auto'
    show_completed = 'yes' if user_profile.show_completed else 'no'

    return render(request, 'settings/settings_home.html', {
        'current_theme_mode': current_theme_mode,
        'show_completed': show_completed,
    })

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
                Status.objects.filter(is_default=True).update(is_default(False))
            form.save()
            return redirect('settings:manage_statuses')
    else:
        form = StatusForm()

    return render(request, 'settings/manage_statuses.html', {'statuses': statuses, 'form': form})

@csrf_exempt
@login_required
def change_theme(request):
    """Change the user's theme preference."""
    if request.method == 'POST':
        theme = request.POST.get('theme')
        if theme in ['light', 'dark', 'auto']:
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.theme_preference = theme
            user_profile.save()
    return redirect('settings:settings_home')
