# Generated by Django 5.0.6 on 2024-06-11 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_alter_task_closed_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='description',
            field=models.TextField(max_length=500, null=True, verbose_name='report'),
        ),
    ]
