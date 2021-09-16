from django.shortcuts import render, redirect
from django.contrib import messages

import requests

from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt




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
    isAuthenticated = False
    req = ''

    def post(self, request):
        if request.method == 'POST':
            if self.isAuthenticated == False:
                Email = request.POST.get('email')
                Password = request.POST.get('password')

                data = {
                    "email": Email,
                    "password": Password
                }
                    
                print(data)

                self.req = requests.post('http://127.0.0.1:8000/api/auth/login', json=data)

                if self.req.status_code == 200:
                    self.isAuthenticated = True
                    messages.success(self.request, 'Successfully Logged in as ' + self.req.json()["first_name"])
                    return redirect('transaction-report')
                messages.warning(self.request, self.req.json()[0])
                return redirect('login')
            elif request.POST.get('logOut') == "true" :
                print("logging out")
                header = {"Authorization": "Token " + self.req.json()["auth_token"]}
                print(header)
                logout_req = requests.post('http://127.0.0.1:8000/api/auth/logout', headers=header)
                if logout_req.status_code == 200:
                    self.isAuthenticated = False
                    messages.success(request, 'Successfully Logged out')
                    return redirect('home')



def transactionReport(request):
    return render(request, "transactions/transaction_report.html")

def Withdraw(request):
    return render(request, "transactions/withdraw.html")

def Deposit(request):
    return render(request, "transactions/deposit.html")