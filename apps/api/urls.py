from django.urls import path
from .views import LikeProductView,ItemCartAPIView

urlpatterns = [
    path('products/<slug:slug>/like/', LikeProductView.as_view(), name='like_product'),
    path('products/<slug:slug>/cart/', ItemCartAPIView.as_view(), name='cart_product'),
]
