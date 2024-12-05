from django.urls import path
from .views import ProductDetailView, ProductListView,FavaritesProductListView

urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("favorites/", FavaritesProductListView.as_view(), name="list-favorites"),
    path("<slug:slug>/", ProductDetailView.as_view(), name="detail"),
]
