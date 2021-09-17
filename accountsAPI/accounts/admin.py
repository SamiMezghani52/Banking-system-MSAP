from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model


user = get_user_model()

class userAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(user, userAdmin)
admin.site.register(UserBankAccount)



