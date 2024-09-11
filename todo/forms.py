# todo/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import TodoItem, Category, Status

class TodoItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            # Set the initial category to the default category if one exists
            default_category = Category.objects.get(is_default=True)
            self.fields['category'].initial = default_category
        except Category.DoesNotExist:
            # No default category is found; handle accordingly if needed
            pass
        
        try:
            # Set the initial status to the default status if one exists
            default_status = Status.objects.get(is_default=True)
            self.fields['status'].initial = default_status
        except Status.DoesNotExist:
            # No default status is found; handle accordingly if needed
            pass

    class Meta:
        model = TodoItem
        fields = ['title', 'description', 'due_date', 'status', 'category']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'is_default']

    def clean_is_default(self):
        """Ensure that only one category can be marked as default."""
        is_default = self.cleaned_data.get('is_default')
        if is_default:
            if Category.objects.filter(is_default=True).exists():
                raise forms.ValidationError('There can only be one default category.')
        return is_default

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name', 'is_default']

    def clean_is_default(self):
        """Ensure that only one status can be marked as default."""
        is_default = self.cleaned_data.get('is_default')
        if is_default:
            if Status.objects.filter(is_default=True).exists():
                raise forms.ValidationError('There can only be one default status.')
        return is_default
