from django.urls import path
from .views import (
    PharmacyCreateView,
    PharmacyUpdateView,
    StockItemCreateView,
    StockItemUpdateView,
)

app_name = "BINA_Q_pharmacies"


urlpatterns = [
    path("pharmacy/new/", PharmacyCreateView.as_view(), name="pharmacy_create"),
    path(
        "pharmacy/<int:pk>/edit/", PharmacyUpdateView.as_view(), name="pharmacy_update"
    ),
    path("stockitem/new/", StockItemCreateView.as_view(), name="stockitem_create"),
    path(
        "stockitem/<int:pk>/edit/",
        StockItemUpdateView.as_view(),
        name="stockitem_update",
    ),
]
