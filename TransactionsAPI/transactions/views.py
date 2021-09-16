from django.shortcuts import render
import datetime
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response 
from rest_framework.parsers import JSONParser 

from .serializers import transactionSerializer
from .models import transactionModel

import requests


def gettransactionAPI(request, id):
    if request.method == 'GET':
        transactions = transactionModel.objects.filter(user_id=id)
        transactions_serializer = transactionSerializer(transactions, many=True)
        return JsonResponse(transactions_serializer.data, safe=False)

@csrf_exempt
def createTransactionAPI(request):
    if request.method == 'POST':

        transaction_data = JSONParser().parse(request)
        account = requests.get('http://127.0.0.1:8000/api/account/'+transaction_data["user_id"]).json()

        print(account)

        new_transactions = transactionModel()
        new_transactions.user_id = account["user"]
        new_transactions.amount = transaction_data["amount"]
        new_transactions.transaction_type = transaction_data["transaction_type"]

        account_data = account

        if new_transactions.transaction_type == "D":
            account_data["balance"] = str(float(account_data["balance"])+float(transaction_data["amount"]))
        else:
            account_data["balance"] = str(float(account_data["balance"])-float(transaction_data["amount"]))

        #if account["initial_deposit_date"] is None:
        #    account_data["initial_deposit_date"] = datetime.datetime.now()
        
        print(account_data)
        
        new_transaction_serializer = transactionSerializer(data = transaction_data)

        if new_transaction_serializer.is_valid():
            new_transaction_serializer.save()
            account_modified = requests.put('http://127.0.0.1:8000/api/accounts/update/', json=account_data)
            print(account_modified)
            if account_modified.status_code == 200:
                message = ["transaction done ..."]
                return JsonResponse(message, safe=False)
        return JsonResponse('Transaction Failed !!!', safe=False)
         

       
            

        
        
