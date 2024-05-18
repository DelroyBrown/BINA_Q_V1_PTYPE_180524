from django import forms
from django.shortcuts import render, redirect
from django.conf import settings
import json


class ProfessionalIdentifierForm(forms.Form):
    identifier = forms.CharField(
        max_length=50,
        required=True,
        label="Professional Identifier",
        widget=forms.TextInput(attrs={"placeholder": "Enter your GMC/NMC/HCPC number"}),
    )
    email = forms.EmailField(
        max_length=255,
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email address"}),
    )

    def clean_identifier(self):
        identifier = self.cleaned_data.get("identifier")
        return identifier

    def clean_email(self):
        email = self.cleaned_data.get("email")
        return email
