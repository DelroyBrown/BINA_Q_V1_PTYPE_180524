from django.db import models
from django.contrib.auth import get_user_model


class Pharmacy(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, default="")
    address = models.CharField(max_length=250, blank=False, null=False, default="")
    phone = models.CharField(max_length=25, blank=False, null=False, default="")
    email = models.EmailField(
        max_length=100, unique=True, null=False, blank=False, default=""
    )
    owner = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class StockItem(models.Model):
    pharmacy = models.ForeignKey(
        Pharmacy, on_delete=models.CASCADE, related_name="stock_items"
    )
    name = models.CharField(max_length=100, blank=False, null=False, default="")
    quantity = models.PositiveIntegerField()
    expiration_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.quantity})"
