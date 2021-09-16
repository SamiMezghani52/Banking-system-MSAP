from . import views
from django.conf.urls import url


urlpatterns = [
    
    url(r'^createAccount/$', views.UserBankAccountsAPI, name='accounts-creation'),
    url(r'^account/([0-9]+)$', views.UserBankAccountsAPI, name='account-information'),
    url(r'^accounts/delete/([0-9]+)$', views.UserBankAccountsAPI, name='account-remove'),
    url(r'^accounts/update/$', views.UserBankAccountsAPI, name='update-account')

]