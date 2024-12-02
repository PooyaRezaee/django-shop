from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from .models import DiscountCode

class DiscountListView(ListView):
    template_name = "cart/discount_code.html"
    model = DiscountCode
    context_object_name = "codes"