from django.test import TestCase

from accounts.models import User
from tasks.models import Task


class TaskCreationTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(
            username='customer@gmail.com',
            first_name='Petr',
            last_name='Fedorov',
            patronymic='Ivanovich',
            email='customer@gmail.com',
            phone='+375333333354',
            role=User.Roles.customer
        )
        Task.objects.create(
            title='test',
            description='task',
            customer=user
        )

    def test_creation(self):
        user = User.objects.get(username='customer@gmail.com')
        self.assertEqual(Task.objects.filter(customer=user).count(), 1)

    def task_have_created_at(self):
        task = Task.objects.get(customer__username='customer@gmail.com')
        self.assertEqual(task.created_at is not None, True)
