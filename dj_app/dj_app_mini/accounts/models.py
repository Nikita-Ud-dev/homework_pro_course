from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

class CourseUserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле "Електронна адреса" є обов`язковим')
        if not phone_number:
            raise ValueError('Поле "Номер телефону" є обов`язковим')

        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have "is_staff=True"')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have "is_superuser=True"')

        return self.create_user(email, phone_number, password, **extra_fields)

# Create your models here.

class CourseUser(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(unique=True, verbose_name='Електронна адреса')
    phone_number = models.CharField(max_length=10, unique=True, blank=True, verbose_name='Номер телефону')
    # password = models.CharField(max_length=20, unique=True, verbose_name='Пароль')
    first_name = models.CharField(max_length=30, verbose_name="Ім'я")
    last_name = models.CharField(max_length=45, verbose_name="Прізвище")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Дата народження')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_staff = models.BooleanField(default=False, verbose_name='Персонал')
    is_active = models.BooleanField(default=True, verbose_name='Активний')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Дата регестрації')
    preffered_language = models.CharField(max_length=10, choices=[
        ('uk', 'Ukrainian'),
        ('us', 'English')
    ], default='uk', verbose_name='Мова')

    objects = CourseUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()







