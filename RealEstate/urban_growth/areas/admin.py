from django.contrib import admin

from .models import Area


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = (
        "area_name",
        "current_price_per_sq_ft",
        "rental_price",
        "number_of_listings",
        "upcoming_infrastructure",
        "distance_from_metro",
        "growth_score",
        "growth_category",
    )
    list_filter = ("upcoming_infrastructure", "growth_category")
    search_fields = ("area_name",)
    readonly_fields = ("growth_score", "growth_category", "created_at")