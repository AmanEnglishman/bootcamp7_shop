from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('У суперпользователя is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('У суперпользователя is_superuser=True')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    class Roles(models.TextChoices):

        BUYER = 'buyer', 'Покупатель'
        SELLER = 'seller', 'Продавец'
        ADMIN = 'admin', 'Администратор'

    email = models.EmailField(unique=True)
    username = None
    full_name = models.CharField(max_length=255)

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.BUYER,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return f'{self.email} - {self.role}'

    @property
    def is_seller(self):
        return self.role == self.Roles.SELLER

    @property
    def is_buyer(self):
        return self.role == self.Roles.BUYER