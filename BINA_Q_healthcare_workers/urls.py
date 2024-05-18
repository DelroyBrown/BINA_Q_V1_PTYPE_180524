from django.urls import path
from . import views

app_name = "BINA_Q_healthcare_workers"


urlpatterns = [
    path("register/", views.register, name="register"),
    path("register/retrieve/", views.retrieve_data, name="retrieve_data"),
    path("register/confirm/", views.confirm_data, name="confirm_data"),
    path(
        "register/complete/", views.complete_registration, name="complete_registration"
    ),
    path("register/success/", views.registration_success, name="registration_success"),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
