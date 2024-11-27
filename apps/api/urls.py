from django.urls import path
from .views import LikeProductView

urlpatterns = [
    path('products/<slug:slug>/like/', LikeProductView.as_view(), name='like_product'),
]
