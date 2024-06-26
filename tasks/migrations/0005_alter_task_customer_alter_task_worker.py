# Generated by Django 5.0.6 on 2024-06-11 17:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_task_description'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_tasks', to=settings.AUTH_USER_MODEL, verbose_name='customer'),
        ),
        migrations.AlterField(
            model_name='task',
            name='worker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='worker_tasks', to=settings.AUTH_USER_MODEL, verbose_name='worker'),
        ),
    ]
