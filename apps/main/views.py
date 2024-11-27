from django.shortcuts import render
from django.views import View
from apps.product.models import Product
from django.db.models import Avg
from .models import Slider

class HomeView(View):
    def get(self, request):
        context = {
            "sliders": Slider.objects.filter(is_visable=True),
            "random_products": Product.objects.filter(is_active=True).annotate(average_score=Avg("comments__score")).order_by("?")[:3],# TODO need use manager and 
            "loop_rating": range(5),
        }

        return render(request, "main\home.html", context)
