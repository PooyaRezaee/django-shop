from django.urls import path
from .views import DiscountListView


urlpatterns = [
    path("discount-codes/", DiscountListView.as_view(), name="discount-codes")
]
