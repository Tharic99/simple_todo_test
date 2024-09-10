# simple_todo/urls.py

# THIS IS THE PROJECT LEVEL URLS.PY FILE

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo.urls')),  # Include the URLs from the 'todo' app
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
