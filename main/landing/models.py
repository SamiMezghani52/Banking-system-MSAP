from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.CharField(primary_key=True, unique=True, max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('First Name', max_length=255, blank=True, null=False)
    last_name = models.CharField('Last Name', max_length=255, blank=True, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} - {self.first_name} {self.last_name}"
