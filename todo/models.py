from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)
    class Meta:
        verbose_name_plural = "status"    

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "categories"    

    def __str__(self):
        return self.name

class TodoItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(null=True, blank=True)  # Allow NULL values
    create_date = models.DateTimeField(default=timezone.now)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Version(models.Model):
    version_number = models.CharField(max_length=20)
    release_date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-release_date']
        verbose_name = "Version"
        verbose_name_plural = "Versions"

    def __str__(self):
        return f"Version {self.version_number} ({self.release_date})"