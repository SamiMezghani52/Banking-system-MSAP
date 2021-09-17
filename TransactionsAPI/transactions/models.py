from django.db import models
from .constants import TRANSACTION_TYPE_CHOICES


class transactionModel(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    transaction_type = models.CharField(choices=TRANSACTION_TYPE_CHOICES, max_length=10)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    timestamp = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)
    
    class Meta:
        ordering = ['timestamp']