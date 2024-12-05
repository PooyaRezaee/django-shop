import uuid
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, TemplateView,DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from apps.product.models import Product
from .models import DiscountCode,OrderItem,Order,Cart
from .utils import add_product_to_cart, reduce_product_from_cart


class DiscountListView(ListView):
    template_name = "cart/discount_code.html"
    model = DiscountCode
    context_object_name = "codes"


class CartView(LoginRequiredMixin, TemplateView):
    template_name = "cart/checkout.html"

    def post(self, request):
        code = request.POST.get("code")
        applied = None
        context = {}
        cart = self.request.user.cart
        if code:
            if DiscountCode.objects.filter(code=code).exists():
                code_obj = DiscountCode.objects.get(code=code)
                applied = "yes" if cart.apply_discount_code(code_obj) else "no"
            else:
                applied = "no"
        
        if applied == "no" and cart.discount_code:
            cart.discount_code = None
            cart.save()
            
        context["applied"] = applied
        context["code"] = code
        return render(request, self.template_name, context)


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


class PaymentView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        cart = user.cart
        
        if not cart.items.exists():
            messages.warning(request, "You don't have item in cart")
            return redirect("main:home")
        
        total, total_after_discount, discount_product, discount_code = cart.total_price
        
        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                customer_code=uuid.uuid4(),
                discount_price=discount_product + discount_code,
                status="P",
                discount_code=cart.discount_code,
            )

            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
                for item in cart.items.all()
            ]

            OrderItem.objects.bulk_create(order_items)
            
            cart.delete()
            Cart.objects.create(user=user)

        messages.success(request,"Successfully completed.")
        return redirect("main:home")
    

class UserOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "cart/orders.html" 
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related("user")


class OrderDetailView(DetailView):
    model = Order
    template_name = "cart/order.html"
    context_object_name = "order"

    def get_object(self):
        return get_object_or_404(Order, pk=self.kwargs["order_id"], user=self.request.user)
