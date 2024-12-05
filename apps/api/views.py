from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.product.models import Product
from apps.cart.utils import add_product_to_cart, reduce_product_from_cart


class LikeProductView(LoginRequiredMixin, View):
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        user = request.user

        if user in product.likes.all():
            return JsonResponse({"detail": "Already liked"}, status=400)

        product.likes.add(user)
        product.save()
        return JsonResponse({"status": "ok"}, status=200)

    def delete(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        user = request.user

        if user not in product.likes.all():
            return JsonResponse({"detail": "Not liked yet"}, status=400)

        product.likes.remove(user)
        product.save()
        return JsonResponse({"status": "ok"}, status=200)


class ItemCartAPIView(LoginRequiredMixin, View):
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        quantity = int(request.POST.get("quantity", 1))
        cart = request.user.cart
        try:
            add_product_to_cart(cart, product, quantity)
            return JsonResponse({"status": "ok"}, status=200)
        except ValueError as e:
            return JsonResponse({"detail": str(e)}, status=400)

    def delete(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        quantity = int(request.POST.get("quantity", 1))
        cart = request.user.cart

        try:
            cart = reduce_product_from_cart(cart, product, quantity)
            return JsonResponse({"status": "ok"}, status=200)
        except ValueError as e:
            return JsonResponse({"detail": str(e)}, status=400)
