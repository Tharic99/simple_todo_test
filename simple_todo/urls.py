# simple_todo/urls.py

# THIS IS THE PROJECT LEVEL URLS.PY FILE

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from registration import views as registration_views  # Import the registration view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo.urls')),  # Include the URLs from the 'todo' app
    path('settings/', include('settings.urls')),  # Include the URLs from the 'settings' app
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', registration_views.register, name='register'),  # Add the registration URL
    path('accounts/', include('django.contrib.auth.urls')),  # Handles default auth URLs
]

# Add static files configuration only in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

