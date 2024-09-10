# Generated by Django 4.2.16 on 2024-09-09 21:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_remove_todoitem_completed_remove_todoitem_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='todoitem',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='todoitem',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='todoitem',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Overdue', 'Overdue')], default='Pending', max_length=10),
        ),
    ]
