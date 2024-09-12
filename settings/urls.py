# settings/urls.py

from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    path('', views.settings_home, name='settings_home'),
    path('categories/', views.manage_categories, name='manage_categories'),
    path('statuses/', views.manage_statuses, name='manage_statuses'),
]
