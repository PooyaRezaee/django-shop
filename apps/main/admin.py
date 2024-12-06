from django.contrib import admin
from .models import Slider


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ("name", "is_visable", "index", "created_at", "updated_at")
    list_filter = ("is_visable", "created_at", "updated_at")
    search_fields = ("name", "link")
    ordering = ("-index",)
    readonly_fields = ("created_at", "updated_at")
    list_editable = ("is_visable", "index")
    fields = (
        "name",
        "image",
        "is_visable",
        "link",
        "index",
        "created_at",
        "updated_at",
    )
