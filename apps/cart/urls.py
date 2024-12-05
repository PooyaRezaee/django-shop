from django.urls import path
from .views import DiscountListView,CartView,AddToCartView,RemoveFromCartView


urlpatterns = [
    path("discount-codes/", DiscountListView.as_view(), name="discount-codes"),
    path("checkout/", CartView.as_view(), name="checkout"),
    path("<slug:product_slug>/add/", AddToCartView.as_view(), name="add-cart"),
    path("<slug:product_slug>/remove/", RemoveFromCartView.as_view(), name="remove-cart"),
]
