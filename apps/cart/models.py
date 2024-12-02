import uuid
from django.db import models


class ProductPack(models.Model):
    POSITION = (
        ("O", "in order"),
        ("C", "in cart"),
    )
    product = models.ForeignKey(
        "product.Product", on_delete=models.CASCADE, related_name="packs"
    )
    quantity = models.PositiveIntegerField(default=1)
    positions = models.CharField(max_length=2, choices=POSITION, default="C")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class Order(models.Model):
    STATUS = (
        ("W", "Wating Payment"),
        ("P", "Pending"),
        ("S", "Success"),
    )
    user = models.ForeignKey(
        "account.User", related_name="orders", on_delete=models.SET_NULL, null=True
    )
    products = models.ManyToManyField(ProductPack, related_name="orders")
    customer_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    total_price = models.FloatField()
    discount_price = models.FloatField(null=True)
    status = models.CharField(max_length=2, choices=STATUS)
    discount_code = models.ForeignKey(
        "DiscountCode", on_delete=models.SET_NULL, related_name="orders", null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.status}"

class Cart(models.Model):
    user = models.ForeignKey(
        "account.User", related_name="carts", on_delete=models.CASCADE, null=True
    )
    products = models.ManyToManyField(ProductPack, related_name="carts")
    discount_code = models.ForeignKey(
        "DiscountCode", on_delete=models.SET_NULL, related_name="carts", null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}"

class DiscountCode(models.Model):
    code = models.CharField(max_length=32)
    minimum_order_price = models.PositiveIntegerField(null=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    expire_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code
