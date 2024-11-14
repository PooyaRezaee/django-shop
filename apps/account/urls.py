from django.urls import path
from .views import CustomLoginView,RegisterView,LogoutView


urlpatterns = [
    path("login/",CustomLoginView.as_view(),name="login"),
    path("register/",RegisterView.as_view(),name="register"),
    path("logout/",LogoutView.as_view(),name="logout"),
]
