from django.views.decorators.csrf import csrf_exempt
from .models import  UserBankAccount
from .utils import create_user_account, get_and_authenticate_user
from . import serializers


from django.http.response import JsonResponse
from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ImproperlyConfigured

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser


User = get_user_model()

class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = serializers.EmptySerializer
    serializer_classes = {
        'login': serializers.UserLoginSerializer,
        'register': serializers.UserRegisterSerializer,
        'password_change': serializers.PasswordChangeSerializer
    }

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(methods=['POST', ], detail=False)
    def logout(self, request):
        logout(request)
        data = {'success': 'Successfully logged out ..'}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated, ])
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer classes should be a dict mapping")
        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


def authenticationTest(request):
    test = JSONParser().parse(request)
    user = User.objects.filter(id=test["id"])
    return Response(data=user.is_authenticated)

@csrf_exempt
def UserBankAccountsAPI(request, id=0):
    if request.method == 'GET':
        user_accounts = UserBankAccount.objects.get(user=id)
        user_accounts_serializer = serializers.UserBankAccountSerializer(user_accounts)
        return JsonResponse(user_accounts_serializer.data, safe=False)

    elif request.method == 'POST':
        user_account_data = JSONParser().parse(request)
        user_accounts_serializer = serializers.UserBankAccountSerializer(data=user_account_data)
        if user_accounts_serializer.is_valid():
            user_accounts_serializer.save()
            return JsonResponse("account created successfully ...", safe=False)
        return JsonResponse("Failed to create account ...", safe=False)

    elif request.method == 'PUT':
        user_account_data = JSONParser().parse(request)
        user_account = UserBankAccount.objects.get(user=user_account_data["user"])
        user_account_serializer = serializers.UserBankAccountSerializer(user_account, data=user_account_data)
        if user_account_serializer.is_valid():
            user_account_serializer.save()
            return JsonResponse("Account Updated successfully ...", safe=False)
        return JsonResponse("Failed to update account ...", safe=False)

    elif request.method == 'DELETE':
        user_account = UserBankAccount.objects.get(account_no=id)
        user_account.delete()
        return JsonResponse("Account Deleted successfully ...", safe=False)

