from django.contrib import admin
from .models import Cart, Order, CartItem, OrderItem, DiscountCode


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "updated_at", "total_price", "discount_code")
    fields = ("user", "discount_code", "created_at", "updated_at")
    list_filter = ("discount_code", "created_at")
    search_fields = ("user__username", "discount_code__code")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "customer_code", "status", "discount_price", "total_price", "created_at")
    fields = ("user", "customer_code", "status", "discount_price", "discount_code", "address", "created_at", "updated_at")
    list_filter = ("status", "discount_code", "created_at")
    search_fields = ("user__username", "customer_code", "discount_code__code")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price", "total_price")
    fields = ("order", "product", "quantity", "price")
    list_filter = ("order", "product")
    search_fields = ("product__name", "order__customer_code")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity", "total_price")
    fields = ("cart", "product", "quantity")
    list_filter = ("cart", "product")
    search_fields = ("product__name", "cart__user__username")


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "minimum_order_price", "discount_price", "expire_at")
    fields = ("code", "minimum_order_price", "discount_price", "expire_at")
    list_filter = ("expire_at",)
    search_fields = ("code",)
