from django import forms
from .models import Pharmacy, StockItem


class PharmacyForm(forms.ModelForm):
    class Meta:
        model = Pharmacy
        fields = [
            "name",
            "address",
            "phone",
            "email",
        ]


class StockItemForm(forms.ModelForm):
    class Meta:
        model = StockItem
        fields = [
            "pharmacy",
            "name",
            "quantity",
            "expiration_date",
        ]
