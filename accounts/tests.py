from django.test import TestCase
from accounts.models import User


class UserCreationTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            username='worker@gmail.com',
            first_name='Fedor',
            last_name='Petrov',
            patronymic='Ivanovich',
            email='worker@gmail.com',
            phone='+375333333333',
            role=User.Roles.worker
        )
        User.objects.create(
            username='customer@gmail.com',
            first_name='Petr',
            last_name='Fedorov',
            patronymic='Ivanovich',
            email='customer@gmail.com',
            phone='+375333333334',
            role=User.Roles.customer
        )

    def test_creation(self):
        self.assertEqual(User.objects.filter(role=User.Roles.worker).count(), 1)
        self.assertEqual(User.objects.filter(role=User.Roles.customer).count(), 1)

    def test_tokens(self):
        user = User.objects.filter(role=User.Roles.worker).first()
        self.assertEqual('access' in user.tokens(), True)
        self.assertEqual('refresh' in user.tokens(), True)
