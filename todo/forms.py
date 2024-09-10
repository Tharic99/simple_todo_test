# todo/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import TodoItem

class TodoItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ['title', 'description', 'due_date', 'status', 'category']  # Include new fields
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'create_date': forms.DateInput(attrs={'type': 'datetime-local'}),  # Optional: For display
        }

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        