from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from .forms import PharmacyForm, StockItemForm
from .models import Pharmacy, StockItem
from django.shortcuts import render


class PharmacyCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = PharmacyForm
    success_url = reverse_lazy("BINA_Q_pharmacies:pharmacy_list")
    template_name = "pharmacy/pharmacy_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PharmacyUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Pharmacy
    form_class = PharmacyForm
    success_url = reverse_lazy("BINA_Q_pharmacies:pharmacy_list")
    template_name = "pharmacy/pharmacy_form.html"


class StockItemCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = StockItemForm
    success_url = reverse_lazy("BINA_Q_pharmacies:pharmacy_detail")
    template_name = "pharmacy/stockitem_form.html"


class StockItemUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = StockItem
    form_class = StockItemForm
    success_url = reverse_lazy("BINA_Q_pharmacies:pharmacy_detail")
    template_name = "pharmacy/stockitem_form.html"
