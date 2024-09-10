from django.db import migrations

def create_default_category(apps, schema_editor):
    Category = apps.get_model('todo', 'Category')
    Category.objects.get_or_create(name='Default')

class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0005_add_default_statuses'),
    ]

    operations = [
        migrations.RunPython(create_default_category),
    ]
