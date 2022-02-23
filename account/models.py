from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models


class UserManager(BaseUserManager):

    def _create(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email я буду указывать?')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        return self._create(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(
        unique=True,
        max_length=24
    )
    email = models.EmailField(
        unique=True
    )
    is_active = models.BooleanField(
        default=False
    )
    activation_code = models.CharField(
        max_length=8,
        blank=True
    )
    '''profile_pic = models.ImageField(
        upload_to='images',
        validators=[FileExtensionValidator(
            ['png', 'jpg', 'jpeg']
        )],
        blank=True,
        null=True
    )'''
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def create_activation_code(self):
        from django.utils.crypto import get_random_string
        code = get_random_string(
            length=8,
            allowed_chars='1234567890qwertyuiop'
        )
        self.activation_code = code

    def __str__(self):
        return self.email





