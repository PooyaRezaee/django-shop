from django.db import transaction
from .models import CartItem
from django.db import transaction

def add_product_to_cart(cart, product, quantity):
    try:
        # if product.stock < quantity:
        #     raise ValueError(f"Only {product.stock} items available in stock.")

        with transaction.atomic():
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={"quantity": quantity}
            )

            if not created:
                cart_item.quantity += quantity
                cart_item.save()

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error adding product to cart: {e}")


def reduce_product_from_cart(cart, product, quantity=1):
    try:
        with transaction.atomic():
            cart_item = CartItem.objects.filter(cart=cart, product=product).first()

            if cart_item:
                if quantity == -1 or quantity >= cart_item.quantity:
                    cart_item.delete()
                else:
                    cart_item.quantity -= quantity
                    cart_item.save()
            else:
                raise ValueError("Product not found in cart.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error removing product from cart: {e}")
