from django.contrib import admin
from .models import Cart, Order, ProductPack, DiscountCode


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductPack)
class CartAdmin(admin.ModelAdmin):
    pass


@admin.register(DiscountCode)
class CartAdmin(admin.ModelAdmin):
    pass