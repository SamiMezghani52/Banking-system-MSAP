from django.urls import path
from . import views


urlpatterns = [
        path('', views.home, name='home'),
        path('register/', views.UserRegister.as_view(), name="register"),
        path('login/', views.userLogin, name='login'),
        path('logout/', views.userLogout, name='logout'),
        path('transaction_report/', views.transactionReport, name='transaction-report'),
        path('withdraw/', views.Withdraw, name='withdraw'),
        path('deposit/', views.Deposit, name='deposit')
    ]