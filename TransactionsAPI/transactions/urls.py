from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^transactions/([0-9]+)$', views.gettransactionAPI, name="get-transactions"),
    url(r'^transactions/create/$', views.createTransactionAPI, name="create-transaction"),
]