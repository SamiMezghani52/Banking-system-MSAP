from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout

import requests

from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt


def home(request):
    if request.method == 'POST':

        email = request.POST.get('Email')
        password = request.POST.get('Password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'logged in successfully as '+ get_user_model().objects.get(email=email).username)
            return redirect('transaction-report')
        else :
            messages.warning(request, 'Failed to log in !!')
            return redirect('home')
    else :
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
            user = get_user_model().objects.create(
                id = req1.json()["id"],
                username = Username,
                email = email,
                first_name = first_name,
                last_name = last_name
            )
            user.set_password(password)
            user.save()
            messages.success(self.request, "Account created successfully !")
            return redirect('login')
        else :
            messages.warning(request, req1.json()[0])
            return redirect('register')

@csrf_exempt
def userLogin(request):
    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        print(user)

        if user is not None:
            login(request, user)
            messages.success(request, 'logged in successfully as '+ get_user_model().objects.get(email=email).username)
            return redirect('transaction-report')
        else :
            messages.warning(request, 'Failed to log in !!')
            return redirect('login')
    else :
        return render(request, 'accounts/user_login.html')
            




def userLogout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')


def transactionReport(request):
    if request.method == 'GET':
        req = requests.get('http://localhost:8002/transactionsAPI/transactions/'+request.user.id)
        user_balance = requests.get('http://127.0.0.1:8000/api/account/'+request.user.id)
        context = {}
        if req.status_code == 200 and user_balance.status_code == 200:
            if req.json() == []:
                messages.warning(request, 'No transactions made')
            else :
                print(req.json())
                context = {
                    "transactions": req.json(),
                    "user_balance": user_balance.json()["balance"]
                }
        
    return render(request, "transactions/transaction_report.html", context)

def Withdraw(request):
    if request.method=='POST':
        amount = request.POST.get('Amount')
        
        transaction_data = {
            "user_id": request.user.id,
            "amount": amount,
            "transaction_type": "W"
        }
        print(transaction_data)
        req = requests.post('http://localhost:8002/transactionsAPI/transactions/create/', json=transaction_data)

        if req.status_code == 200:
            messages.success(request, amount+'$ Withdraw success')
            return redirect('transaction-report')
        else :
            messages.warning(request,'Withdraw failed')
    return render(request, "transactions/withdraw.html")

def Deposit(request):
    if request.method=='POST':
        Amount = request.POST.get('amount')
        
        transaction_data = {
            "user_id": request.user.id,
            "amount": Amount,
            "transaction_type": "D"
        }
        print(transaction_data)
        req = requests.post('http://localhost:8002/transactionsAPI/transactions/create/', json=transaction_data)

        if req.status_code == 200:
            messages.success(request, Amount+'$ Deposit success')
            return redirect('transaction-report')
        else :
            messages.warning(request,'Deposit failed')
    return render(request, "transactions/deposit.html")