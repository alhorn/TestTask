from django.db import models


class Task(models.Model):
    class Statuses(models.TextChoices):
        TO_DO = 'to_do', 'to_do'
        IN_PROGRESS = 'in_progress', 'in_progress'
        COMPLETED = 'completed', 'completed'

    worker = models.ForeignKey(
        verbose_name='worker', to='accounts.User',
        on_delete=models.CASCADE, related_name='worker_tasks', null=True, blank=True
    )
    customer = models.ForeignKey(
        verbose_name='customer', to='accounts.User',
        on_delete=models.CASCADE, related_name='customer_tasks', null=True, blank=True
    )
    created_at = models.DateTimeField(verbose_name='created at', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='updated at', auto_now=True)
    closed_at = models.DateTimeField(verbose_name='closed at', null=True)
    status = models.CharField(
        verbose_name='status', max_length=11,
        choices=Statuses.choices, default=Statuses.TO_DO
    )
    title = models.CharField(verbose_name='title', max_length=255, null=True)
    description = models.TextField(verbose_name='report', null=True, blank=True)
    report = models.TextField(verbose_name='report', null=True, blank=True)

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return f'{self.id}'
