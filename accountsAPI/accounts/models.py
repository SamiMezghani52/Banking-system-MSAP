from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

from decimal import Decimal
from .constants import GENDER_CHOICE

class BankAccountType(models.Model):
    name = models.CharField(max_length=100)
    maximum_withdrawal_amount = models.DecimalField(decimal_places=2, max_digits=12)
    
class UserBankAccount(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    account_type = models.ForeignKey(BankAccountType, related_name='accounts', on_delete=models.CASCADE)
    account_no = models.PositiveIntegerField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    initial_deposit_date = models.DateField(null=True, blank=True)


