from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from apps.product.models import Product
from .models import DiscountCode
from .utils import add_product_to_cart, reduce_product_from_cart


class DiscountListView(ListView):
    template_name = "cart/discount_code.html"
    model = DiscountCode
    context_object_name = "codes"


class CartView(LoginRequiredMixin, TemplateView):
    template_name = "cart/checkout.html"


class AddToCartView(LoginRequiredMixin, TemplateView):
    def get(self, request, product_slug, *args, **kwargs):
        quantity = int(request.GET.get("quantity", 1))
        product = Product.objects.get(slug=product_slug)
        cart = request.user.cart
        try:
            add_product_to_cart(cart, product, quantity)
        except ValueError as e:
            messages.warning(request, str(e))

        return redirect("cart:checkout")


class RemoveFromCartView(LoginRequiredMixin, TemplateView):
    def get(self, request, product_slug, *args, **kwargs):
        product = Product.objects.get(slug=product_slug)
        quantity = int(request.GET.get("quantity", 1))
        cart = request.user.cart

        try:
            cart = reduce_product_from_cart(cart, product, quantity)
        except ValueError as e:
            messages.warning(request, str(e))
        return redirect("cart:checkout")


class CheckOutView(View):
    def get(self, request):
        pass


class PaymentView(View):
    pass
