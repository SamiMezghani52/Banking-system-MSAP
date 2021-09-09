from .models import BankAccountType, UserBankAccount
from .serializers import UserSerializer, RegisterSerializer, BankAccountTypeSerializer, UserBankAccountSerializer

from django.http.response import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.models import User

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.parsers import JSONParser

from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


def userAPI(request, id=0):
    if request.method == 'GET':
        user_information = User.objects.get(id=id)
        user_serializer = UserSerializer(user_information)
        return JsonResponse(user_serializer.data, safe=False)
    
    elif request.method == 'POST':
        user = JSONParser.parse(request)
        user_data = User.objects.get(id=user['id'])
        user_serializer = UserSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse('User updated successfully ...', safe=False)
        return JsonResponse('Failed to update user ...', safe=False)

    elif request.method == 'DELETE':
        user = User.objects.get(id=id)
        user.delete()
        return JsonResponse('User successfully deleted ...', safe=False)

def BankAcountTypeAPI(request):
    if request.method == 'GET':
        account_types = BankAccountType.objects.all()
        account_types_serializer = BankAccountTypeSerializer(account_types, many=True)
        return JsonResponse(account_types_serializer.data, safe=False)

def UserBankAccountsAPI(request, id=0, user=''):
    if request.method == 'GET':
        user_accounts = UserBankAccount.objects.get(account_no=id)
        user_accounts_serializer = UserBankAccountSerializer(user_accounts)
        return JsonResponse(user_accounts_serializer.data, safe=False)

    elif request.method == 'POST':
        user_account_data = JSONParser().parse(request)
        user_accounts_serializer = (user_account_data)
        if user_accounts_serializer.is_valid():
            user_accounts_serializer.save()
            return JsonResponse("account created successfully ...", safe=False)
        return JsonResponse("Failed to create account ...", safe=False)

    elif request.method == 'PUT':
        user_account_data = JSONParser().parse(request)
        user_account = UserBankAccount.objects.get(account_no=user_account_data["account_no"])
        user_account_serializer = UserBankAccountSerializer(user_account, data=user_account_data)
        if user_account_serializer.is_valid():
            user_account_serializer.save()
            return JsonResponse("Account Updated successfully ...", safe=False)
        return JsonResponse("Failed to update account ...", safe=False)

    elif request.method == 'DELETE':
        user_account = UserBankAccount.objects.get(account_no=id)
        user_account.delete()
        return JsonResponse("Account Deleted successfully ...", safe=False)

