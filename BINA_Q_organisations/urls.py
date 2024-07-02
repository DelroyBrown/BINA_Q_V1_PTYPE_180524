# BINA_Q_organisations/urls.py
from django.urls import path
from . import views

app_name = "BINA_Q_organisations"


urlpatterns = [
    path(
        "members/",
        views.organisation_members,
        name="organisation_members",
    ),
]
