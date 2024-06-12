from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.managers import UserManager


class ImageFile(models.Model):
    image = models.ImageField('image', upload_to='images/')
    created_at = models.DateTimeField(verbose_name='created at', auto_now_add=True)

    class Meta:
        verbose_name = 'Image File'
        verbose_name_plural = 'Image Files'


class User(AbstractUser):
    class Roles(models.TextChoices):
        worker = 'worker', 'worker'
        customer = 'customer', 'customer'

    username = models.CharField(
        'username',
        max_length=150, unique=True,
        error_messages={
            'unique': "A user with that username already exists."
        }
    )
    first_name = models.CharField('first name', max_length=150)
    last_name = models.CharField('last name', max_length=150)
    patronymic = models.CharField('patronymic', max_length=150)
    email = models.EmailField('email address', unique=True)
    phone = models.CharField(verbose_name='phone', max_length=255, unique=True)
    avatar = models.ForeignKey(
        to=ImageFile,
        verbose_name='avatar',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_avatar'
    )
    role = models.CharField('role', max_length=8, choices=Roles.choices, default=Roles.worker)
    is_can_create_tasks = models.BooleanField(verbose_name='is_can_create_tasks', default=False)
    is_have_access_to_tasks = models.BooleanField(verbose_name='is_have_access_to_tasks', default=False)
    is_can_add_customers = models.BooleanField(verbose_name='is_can_add_customers', default=False)
    is_can_add_workers = models.BooleanField(verbose_name='is_can_add_workers', default=False)
    is_have_access_to_workers = models.BooleanField(verbose_name='is_have_access_to_workers', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.email}'

    def tokens(self):
        refresh = RefreshToken.for_user(user=self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def save(self, *args, **kwargs):
        if self.role == self.Roles.customer:
            self.is_can_create_tasks = False
            self.is_have_access_to_tasks = False
            self.is_can_add_customers = False
            self.is_can_add_workers = False
        else:
            self.is_have_access_to_workers = False
        super().save()
