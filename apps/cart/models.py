import uuid
from django.db import models


class CartItem(models.Model):
    cart = models.ForeignKey("Cart", related_name="items", on_delete=models.CASCADE, db_index=True)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity}) in cart of {self.cart.user}"

    @property
    def total_price(self):
        return self.product.price * self.quantity

    @property
    def total_price_after_discount(self):
        if self.product.price_after_discount:
            return self.product.price_after_discount * self.quantity
        else:
            return self.total_price

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        ordering = ["cart", "product"]
        unique_together = ('cart', 'product')


class OrderItem(models.Model):
    order = models.ForeignKey("Order", related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity}) in order of {self.order.user}"

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        ordering = ["order", "product"]


class Order(models.Model):
    STATUS = (
        ("W", "Waiting Payment"),
        ("P", "Pending"),
        ("S", "Success"),
    )
    user = models.ForeignKey(
        "account.User", related_name="orders", on_delete=models.SET_NULL, null=True
    )
    customer_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.CharField(max_length=2, choices=STATUS)
    discount_code = models.ForeignKey(
        "DiscountCode", on_delete=models.SET_NULL, related_name="orders", null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return sum(item.quantity * item.price for item in self.items.all())

    def __str__(self):
        return f"{self.user} - {self.status}"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]


class Cart(models.Model):
    user = models.OneToOneField(
        "account.User", related_name="cart", on_delete=models.CASCADE, null=True
    )
    discount_code = models.ForeignKey(
        "DiscountCode", on_delete=models.SET_NULL, related_name="carts", null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user}"

    @property
    def total_price(self):
        # total,after_discount,discount
        total = 0
        total_after_discount = 0

        for item in self.items.all():
            quantity = item.quantity
            total += item.product.price * quantity
            if item.product.price_after_discount:
                total_after_discount += item.product.price_after_discount * quantity
            else:
                total_after_discount += item.product.price * quantity

        discount = total - total_after_discount

        if self.discount_code:
            pass

        return total, total_after_discount, discount

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"


class DiscountCode(models.Model):
    code = models.CharField(max_length=32, unique=True)
    minimum_order_price = models.PositiveIntegerField(null=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    expire_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_valid(self):
        from django.utils.timezone import now

        return now() < self.expire_at

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Discount Code"
        verbose_name_plural = "Discount Codes"
        ordering = ["-expire_at"]
