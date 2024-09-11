from django.contrib import admin
from .models import TodoItem, Category, Status, Version

class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'status', 'create_date', 'category', 'user')  # Fields to display in list view
    list_filter = ('status', 'category', 'user')  # Fields to filter by in the admin list view
    search_fields = ('title', 'description')  # Fields to search by
    readonly_fields = ('create_date',)  # Fields that should be read-only

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_default')
    list_editable = ('is_default',)
    actions = ['make_default']

    def make_default(self, request, queryset):
        """Custom action to set a category as default and unset others."""
        if queryset.count() > 1:
            self.message_user(request, "You can only select one category to make default.", level='error')
            return

        Category.objects.filter(is_default=True).update(is_default=False)
        queryset.update(is_default=True)
        self.message_user(request, "Category successfully set as default.")

    make_default.short_description = "Set selected category as default"

class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_default')
    list_editable = ('is_default',)
    actions = ['make_default']

    def make_default(self, request, queryset):
        """Custom action to set a status as default and unset others."""
        if queryset.count() > 1:
            self.message_user(request, "You can only select one status to make default.", level='error')
            return

        Status.objects.exclude(id__in=queryset.values('id')).update(is_default=False)
        queryset.update(is_default=True)
        self.message_user(request, "Status successfully set as default.")

    make_default.short_description = "Set selected status as default"


class VersionAdmin(admin.ModelAdmin):
    list_display = ('version_number', 'release_date', 'description')
    ordering = ('-release_date',)
    search_fields = ('version_number', 'description')

# Register the remaining models
admin.site.register(TodoItem, TodoItemAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Version, VersionAdmin)
