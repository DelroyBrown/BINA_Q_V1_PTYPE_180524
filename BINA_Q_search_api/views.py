# BINA_Q_search_api/views.py
from rest_framework import generics
from BINA_Q_healthcare_workers.models import HealthcareWorker
from .search_serializer import HealthcareWorkerSerializer


class HealthcareWorkerList(generics.ListAPIView):
    queryset = HealthcareWorker.objects.all()
    serializer_class = HealthcareWorkerSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        first_name = self.request.query_params.get("first_name")
        if first_name:
            queryset = queryset.filter(user__first_name__icontains=first_name)

        last_name = self.request.query_params.get("last_name")
        if last_name:
            queryset = queryset.filter(user__last_name__icontains=last_name)

        specialization = self.request.query_params.get("specialization")
        if specialization:
            queryset = queryset.filter(specialization__icontains=specialization)

        organisation_affiliation = self.request.query_params.get(
            "organisation_affiliation"
        )
        if organisation_affiliation:
            queryset = queryset.filter(
                organisation_affiliation__icontains=organisation_affiliation
            )

        ods_code = self.request.query_params.get("ods_code")
        if ods_code:
            queryset = queryset.filter(ods_code__icontains=ods_code)

        return queryset
