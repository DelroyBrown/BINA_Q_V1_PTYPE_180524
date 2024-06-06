# BINA_Q_users/forms.py
from django import forms
from BINA_Q_healthcare_workers.models import HealthcareWorker
from .models import User


class LoginForm(forms.Form):
    bina_q_id = forms.CharField(max_length=50, label="BINA-Q-ID")
    password = forms.CharField(widget=forms.PasswordInput)


class PasswordChangeForm(forms.Form):
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="New Password")
    new_password2 = forms.CharField(
        widget=forms.PasswordInput, label="Confirm New Password"
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data


class DashboardUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user_id = self.instance.id

        if User.objects.filter(email=email).exclude(id=user_id).exists():
            raise forms.ValidationError("This email is already in use.")
        return email


class ODSCodeUpdateForm(forms.ModelForm):
    class Meta:
        model = HealthcareWorker
        fields = ["ods_code"]
