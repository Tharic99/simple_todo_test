from django.db import migrations

def create_default_statuses(apps, schema_editor):
    Status = apps.get_model('todo', 'Status')
    default_statuses = ['Pending', 'Completed', 'Overdue']
    for status in default_statuses:
        Status.objects.get_or_create(name=status)

class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_status_alter_todoitem_category_alter_todoitem_status'),
    ]

    operations = [
        migrations.RunPython(create_default_statuses),
    ]


