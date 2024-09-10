from django.contrib import admin
from .models import TodoItem, Category, Status, Version

class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'status', 'create_date', 'category', 'user')  # Fields to display in list view
    list_filter = ('status', 'category', 'user')  # Fields to filter by in the admin list view
    search_fields = ('title', 'description')  # Fields to search by
    readonly_fields = ('create_date',)  # Fields that should be read-only

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Fields to display in list view
    search_fields = ('name',)  # Fields to search by

class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Fields to display in list view
    search_fields = ('name',)  # Fields to search by


class VersionAdmin(admin.ModelAdmin):
    list_display = ('version_number', 'release_date', 'description')
    ordering = ('-release_date',)
    search_fields = ('version_number', 'description')

admin.site.register(TodoItem, TodoItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Version, VersionAdmin)