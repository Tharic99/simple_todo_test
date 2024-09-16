# settings/forms.py

from django import forms
from todo.models import Category, Status
from .models import UserProfile

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

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['theme_preference']