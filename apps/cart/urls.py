from django.urls import path
from .views import (
    DiscountListView,
    CartView,
    AddToCartView,
    RemoveFromCartView,
    PaymentView,
    UserOrderListView,
    OrderDetailView,
)


urlpatterns = [
    path("discount-codes/", DiscountListView.as_view(), name="discount-codes"),
    path("checkout/", CartView.as_view(), name="checkout"),
    path("payment/", PaymentView.as_view(), name="payment"),
    path("<slug:product_slug>/add/", AddToCartView.as_view(), name="add-cart"),
    path(
        "<slug:product_slug>/remove/", RemoveFromCartView.as_view(), name="remove-cart"
    ),
    path("orders/", UserOrderListView.as_view(), name="orders"),
    path("order/<int:order_id>/", OrderDetailView.as_view(), name="order"),
]
