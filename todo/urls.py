# todo/urls.py

# THIS IS THE APP LEVEL URLS.PY FILE

from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('edit/<int:pk>/', views.edit_todo, name='edit_todo'),
    path('add/', views.add_todo, name='add_todo'),
    path('delete/<int:pk>/', views.confirm_delete, name='confirm_delete'),
    path('update_task_status/', views.update_task_status, name='update_task_status'),
    
    # URL patterns for adding or editing categories
    path('categories/add/', views.add_or_edit_category, name='add_category'),
    path('categories/edit/<int:pk>/', views.add_or_edit_category, name='edit_category'),
]
