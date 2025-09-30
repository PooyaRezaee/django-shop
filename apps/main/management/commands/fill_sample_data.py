import os
from django.core.management.base import BaseCommand
from apps.account.models import User,Addresses
from apps.main.models import Slider
from django.core.files import File
from django.utils.text import slugify
from apps.product.models import Product, Category, Comment
from django.db import IntegrityError
from apps.cart.models import DiscountCode
from django.utils import timezone
from datetime import timedelta

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")  


class Command(BaseCommand):
    help = "Fill database with sample data"

    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.SUCCESS("Accounts data ..."))
            admin = User.objects.create_superuser("admin@gmail.com", "admin1234")
            user1 = User.objects.create_user("michael@gmail.com", "user1234")
            user2 = User.objects.create_user("sarah@gmail.com", "user1234")
            user3 = User.objects.create_user("james@gmail.com", "user1234")
            Addresses.objects.create(
                user=user1,
                title="Home",
                province="California",
                city="Los Angeles",
                postal_address="123 Hollywood Blvd",
                phone_number="1234567890",
                zipcode=90001,
            )
            Addresses.objects.create(
                user=user1,
                title="Office",
                province="California",
                city="Los Angeles",
                postal_address="456 Office Street",
                phone_number="9876543210",
                zipcode=90002,
            )

            Addresses.objects.create(
                user=user2,
                title="Home",
                province="Texas",
                city="Houston",
                postal_address="789 Main Street",
                phone_number="1231231234",
                zipcode=77001,
            )

            Addresses.objects.create(
                user=user3,
                title="Home",
                province="New York",
                city="New York City",
                postal_address="321 Broadway Ave",
                phone_number="5554443333",
                zipcode=10001,
            )
        except IntegrityError:
            pass
        
        try:
            self.stdout.write(self.style.SUCCESS("Product data ..."))
            electronics, _ = Category.objects.get_or_create(name="Electronics")
            books, _ = Category.objects.get_or_create(name="Books")
            clothes, _ = Category.objects.get_or_create(name="Clothes")

            products_data = [
                {
                    "name": "Samsung Galaxy S25 Plus",
                    "price": 999,
                    "price_after_discount": 899,
                    "stock": 50,
                    "category": electronics,
                    "image_address": "galexy.png",
                    "description": "Latest Samsung Galaxy with amazing features.",
                },
                {
                    "name": "Samsung Galaxy S25 Ultra",
                    "price": 950,
                    "price_after_discount": 870,
                    "stock": 40,
                    "category": electronics,
                    "image_address": "galexy.png",
                    "description": "High-end Samsung smartphone with great camera.",
                },
                {
                    "name": "Apple Watch Series 9",
                    "price": 1200,
                    "price_after_discount": 980,
                    "stock": 20,
                    "category": electronics,
                    "image_address": "watch.png",
                    "description": "Powerful watch for professionals.",
                },
                {
                    "name": "The Great Gatsby",
                    "price": 20,
                    "price_after_discount": 15,
                    "stock": 100,
                    "category": books,
                    "image_address": "book.jpg",
                    "description": "Classic novel by F. Scott Fitzgerald.",
                },
                {
                    "name": "Harry Potter Box Set",
                    "price": 80,
                    "price_after_discount": 70,
                    "stock": 60,
                    "category": books,
                    "image_address": "book.jpg",
                    "description": "Complete collection of the Harry Potter series.",
                },
                {
                    "name": "Nike Air Jordan 1",
                    "price": 150,
                    "price_after_discount": 130,
                    "stock": 35,
                    "category": clothes,
                    "image_address": "clothes.png",
                    "description": "Popular sneakers for sports and casual wear.",
                },
                {
                    "name": "Adidas T-Shirt",
                    "price": 25,
                    "price_after_discount": 20,
                    "stock": 80,
                    "category": clothes,
                    "image_address": "clothes.png",
                    "description": "Comfortable cotton t-shirt for everyday use.",
                },
                {
                    "name": "Levi's 501 Jeans",
                    "price": 60,
                    "price_after_discount": 50,
                    "stock": 70,
                    "category": clothes,
                    "image_address": "clothes.png",
                    "description": "Classic straight-leg denim jeans.",
                },
            ]

            for item in products_data:
                slug = slugify(item["name"])
                if Product.objects.filter(slug=slug).exists():
                    continue

                product = Product(
                    name=item["name"],
                    slug=slug,
                    description=item["description"],
                    price=item["price"],
                    price_after_discount=item["price_after_discount"],
                    stock=item["stock"],
                    category=item["category"],
                    is_active=True,
                )

                image_path = os.path.join(ASSETS_DIR, item["image_address"])
                if os.path.exists(image_path):
                    with open(image_path, "rb") as f:
                        product.image.save(f"{slug}.jpg", File(f), save=False)

                product.save()
        except IntegrityError:
            pass

        try:
            self.stdout.write(self.style.SUCCESS("Slider data ..."))
            sliders_data = [
                {
                    "name": "Summer Sale 2025",
                    "index": 1,
                    "image_address": "SummerBanner.jpg",
                    "link": "/products/?category=clothes",
                },
                {
                    "name": "New Product",
                    "index": 2,
                    "image_address": "NewProductBanner.webp",
                }
            ]

            for item in sliders_data:
                if Slider.objects.filter(index=item["index"]).exists():
                    continue

                slider = Slider(
                    name=item["name"],
                    link=item.get("link"),
                    index=item["index"],
                    is_visable=True,
                )

                image_path = os.path.join(ASSETS_DIR, item["image_address"])
                if os.path.exists(image_path):
                    with open(image_path, "rb") as f:
                        slider.image.save(f"slider_{item['index']}.jpg", File(f), save=False)

                slider.save()
        except IntegrityError:
            pass

        try:
            self.stdout.write(self.style.SUCCESS("Discount Code data ..."))
            codes_data = [
                {
                    "code": "WELCOME10",
                    "minimum_order_price": 20,
                    "discount_price": 10,
                    "expire_at": timezone.now() + timedelta(days=30),
                },
                {
                    "code": "SAVE20",
                    "minimum_order_price": 100,
                    "discount_price": 20,
                    "expire_at": timezone.now() + timedelta(days=15),
                },
                {
                    "code": "BIGSALE50",
                    "minimum_order_price": 200,
                    "discount_price": 50,
                    "expire_at": timezone.now() + timedelta(days=10),
                },
                {
                    "code": "FREESHIP",
                    "minimum_order_price": 50,
                    "discount_price": 15,
                    "expire_at": timezone.now() + timedelta(days=60),
                },
                {
                    "code": "SUMMER25",
                    "minimum_order_price": 150,
                    "discount_price": 25,
                    "expire_at": timezone.now() + timedelta(days=20),
                },
            ]

            for item in codes_data:
                if not DiscountCode.objects.filter(code=item["code"]).exists():
                    DiscountCode.objects.create(
                        code=item["code"],
                        minimum_order_price=item["minimum_order_price"],
                        discount_price=item["discount_price"],
                        expire_at=item["expire_at"],
                    )
        except IntegrityError:
            pass

        try:
            self.stdout.write(self.style.SUCCESS("Comments data ..."))

            users = list(User.objects.all())

            # Hardcoded comment texts
            comment_texts = [
                "Excellent product, highly recommend!",
                "Good quality, fast delivery.",
                "Not satisfied with the product.",
                "Amazing! Exceeded my expectations.",
                "Decent product for the price.",
                "Would buy again.",
                "Five stars, perfect!",
                "Could be better, but okay overall.",
                "Loved it! Works perfectly.",
            ]

            # Assign comments to each product
            for product in Product.objects.all():
                for i, user in enumerate(users):
                    # Cycle through comment_texts to assign different comments
                    text = comment_texts[(product.id + i) % len(comment_texts)]
                    score = ((product.id + i) % 5) + 1  # score between 1-5

                    # Avoid duplicate
                    if not Comment.objects.filter(user=user, product=product, comment=text).exists():
                        Comment.objects.create(
                            user=user,
                            product=product,
                            comment=text,
                            score=score
                        )
        except IntegrityError:
            pass

        self.stdout.write(self.style.SUCCESS("Sample data inserted successfully!"))
