from django.contrib import admin
from .models import Cart, Order, CartItem, OrderItem, DiscountCode


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    pass

@admin.register(DiscountCode)
class CartAdmin(admin.ModelAdmin):
    pass
