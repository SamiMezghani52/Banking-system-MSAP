from django.urls import path
from . import views


urlpatterns = [
        path('', views.home, name='home'),
        path('register/', views.UserRegister.as_view(), name="register"),
        path('login/', views.userLoginView.as_view(), name='login'),
        #path('transaction_report/', views.transactionReport, name='transaction-report')
    ]