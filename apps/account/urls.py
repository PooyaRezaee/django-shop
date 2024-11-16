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
    ChangePasswordView,
    ResetPasswordView,
    RequestResetPasswordView,
)


urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password/change/", ChangePasswordView.as_view(), name="password-change"),
    path("password/reset/request/", RequestResetPasswordView.as_view(), name="password-request-reset"),
    path("password/reset/<str:uidb64>/<str:token>/", ResetPasswordView.as_view(), name="password-reset"),
    path("profile/", UpdateProfileView.as_view(), name="profile"),
    path("address/list/", AddresseListView.as_view(), name="address-list"),
    path("address/delete/<int:pk>/", AddressDeleteView.as_view(), name="address-delete"),
    path("address/add/", AddressCreateView.as_view(), name="address-add"),
    path("address/modify/<int:pk>/", AddresseUpdateView.as_view(), name="address-update"),
]
