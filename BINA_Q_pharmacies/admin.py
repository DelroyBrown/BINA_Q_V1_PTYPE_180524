from django.contrib import admin
from .models import Pharmacy, StockItem


@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "address",
        "phone",
        "email",
        "owner",
    )


@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = (
        "pharmacy",
        "name",
        "quantity",
        "expiration_date",
    )
