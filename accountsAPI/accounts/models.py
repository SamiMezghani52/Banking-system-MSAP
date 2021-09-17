from django.db import models
from django.contrib.auth.models import AbstractUser

from .constants import GENDER_CHOICE

class User(AbstractUser):
    id = models.AutoField(primary_key=True, unique=True)
    username = models.CharField(max_length=100)
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('First Name', max_length=255, blank=True, null=False)
    last_name = models.CharField('Last Name', max_length=255, blank=True, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} - {self.first_name} {self.last_name}"

    
class UserBankAccount(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    account_no = models.PositiveIntegerField()
    maximum_withdrawal_amount =  models.DecimalField(decimal_places=2, max_digits=12)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    balance = models.DecimalField(decimal_places=2, max_digits=12)
    initial_deposit_date = models.DateField(null=True, blank=True)


