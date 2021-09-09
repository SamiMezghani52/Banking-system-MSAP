from . import views
from django.conf.urls import url

from knox import views as knox_views

urlpatterns = [
    url(r'^register/$', views.RegisterAPI.as_view(), name='register'),
    url(r'^login/$', views.LoginAPI.as_view(), name='login'),
    url(r'^logout/$', knox_views.LogoutView.as_view(), name='logout'),
    
    url(r'^user/([0-9]+)$', views.userAPI, name='user-information'),

    url(r'^accountTypes/$', views.BankAcountTypeAPI, name='account-types'),

    url(r'^createAccount/$', views.UserBankAccountsAPI, name='accounts-creation'),
    url(r'^account/([0-9]+)$', views.UserBankAccountsAPI, name='accounts-list'),
    url(r'^accounts/delete/([0-9]+)$', views.UserBankAccountsAPI, name='account-remove')

]