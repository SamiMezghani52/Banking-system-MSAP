from .models import transactionModel
from rest_framework import serializers

class transactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = transactionModel
        fields = (
            'user_id', 
            'amount',
            'transaction_type',
        )
