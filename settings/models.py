from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme_preference = models.CharField(max_length=10, choices=[('light', 'Light'), ('dark', 'Dark'), ('auto', 'Auto')], default='auto')
    show_completed = models.BooleanField(default=False)
    enable_confirmations = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
