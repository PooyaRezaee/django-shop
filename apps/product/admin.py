from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "path", "created_at")
    search_fields = ("name", "path")
    list_filter = ("parent", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("path", "created_at")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "image_display",
        "category",
        "price",
        "price_after_discount",
        "stock",
        "is_active",
        "created_at",
    )
    list_filter = ("category", "is_active", "created_at")
    search_fields = ("name", "description")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    prepopulated_fields = {'slug': ('name',), }

    def image_display(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 100px; object-fit: cover;" />',
                obj.image.url,
            )
        return "No Image"

    image_display.short_description = "Image"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "score", "created_at")
    list_filter = ("score", "created_at")
    search_fields = ("comment",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
