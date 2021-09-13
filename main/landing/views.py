from django.shortcuts import render, redirect
from django.contrib import messages
import requests

from django.views.generic import TemplateView





def home(request):
    return render(request, "core/index.html")

class UserRegister(TemplateView):
    template_name = "accounts/user_registration.html"

    def post(self, request):
        if request.method == 'POST':
            Username = request.POST.get('userName')
            email = request.POST.get('Email')
            password = request.POST.get('password')
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            Gender = request.POST.get('gender')
            maximum_withdrawal_amount = request.POST.get('maximumWithdrawalAmount')
            account_no = request.POST.get('accountNumber')

            data = { 
                "username": Username,
                "email": email,
                "password": password,
                "first_name": first_name,
                "last_name": last_name
            }

            req1 = requests.post('http://127.0.0.1:8000/api/auth/register', json=data)

            print(req1.json())

            account_data = {
                "user": req1.json()["id"],
                "account_no": account_no,
                "maximum_withdrawal_amount": maximum_withdrawal_amount,
                "gender": Gender,
                "balance": "0",
                "initial_deposit_date": None
            }
            req2 = requests.post('http://127.0.0.1:8000/api/createAccount/', json=account_data)

        if req2.status_code == 200: 
            print(req2.json())
            messages.success(self.request, "Account created successfully !")
            return redirect('login')
        return redirect('home')


class userLoginView(TemplateView):
    template_name="accounts/user_login.html"
    auth_token = ''
    
    def login(self, request):
        pass
    