from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.product.models import Product


class LikeProductView(LoginRequiredMixin, View):
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        user = request.user

        if user in product.likes.all():
            return JsonResponse({"message": "Already liked"}, status=400)

        product.likes.add(user)
        product.save()
        return JsonResponse({"status": "liked"}, status=200)

    def delete(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        user = request.user

        if user not in product.likes.all():
            return JsonResponse({"message": "Not liked yet"}, status=400)

        product.likes.remove(user)
        product.save()
        return JsonResponse({"status": "unliked"}, status=200)
