from django.urls import path
from .views import (
    CustomLoginView,
    RegisterView,
    LogoutView,
    UpdateProfileView,
    AddressCreateView,
    AddresseListView,
    AddressDeleteView,
    AddresseUpdateView,
)


urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", UpdateProfileView.as_view(), name="profile"),
    path("address/list/", AddresseListView.as_view(), name="address-list"),
    path("address/delete/<int:pk>/", AddressDeleteView.as_view(), name="address-delete"),
    path("address/add/", AddressCreateView.as_view(), name="address-add"),
    path("address/modify/<int:pk>/", AddresseUpdateView.as_view(), name="address-update"),
]
