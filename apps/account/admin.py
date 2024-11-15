from django.contrib import admin
from .models import User,Addresses


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Addresses)
class AddressAdmin(admin.ModelAdmin):
    pass
