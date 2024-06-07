from django.urls import path
from .views import HealthcareWorkerList

app_name = "BINA_Q_search_api"

urlpatterns = [
    path(
        "healthcare_workers/",
        HealthcareWorkerList.as_view(),
        name="healthcare_worker_list",
    ),
]
