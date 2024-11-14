from django.shortcuts import redirect
from django.urls import reverse

class NoLoginMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("main:home"))
        return super().dispatch(request, *args, **kwargs)
        