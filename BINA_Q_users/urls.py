# BINA_Q_users/urls.py
from django.urls import path
from .views import (
    login_view,
    password_change_view,
    check_temporary_password,
    logout_confirmation_view,
    logout_view,
    dashboard_update_view,
    fetch_ods_details,
)

app_name = "BINA_Q_users"


urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/confirm/", logout_confirmation_view, name="logout_confirmation"),
    path("logout/", logout_view, name="logout"),
    path("password_change/", password_change_view, name="password_change"),
    path(
        "check_temporary_password/",
        check_temporary_password,
        name="check_temporary_password",
    ),
    path("dashboard/edit/", dashboard_update_view, name="dashboard_update"),
    path("fetch_ods_details/", fetch_ods_details, name="fetch_ods_details"),
]
