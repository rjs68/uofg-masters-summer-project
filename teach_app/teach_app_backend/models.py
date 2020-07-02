from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from teach_app_backend.managers import TeachUserManager


class TeachUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    profile_picture = models.ImageField(upload_to='profile_pictures')

    is_teacher = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = TeachUserManager()

    def __str__(self):
        return self.email
