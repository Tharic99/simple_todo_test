# Generated by Django 4.2.16 on 2024-09-16 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0013_alter_category_options_alter_todoitem_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='todoitem',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
