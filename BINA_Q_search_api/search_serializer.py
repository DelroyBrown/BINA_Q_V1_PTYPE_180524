# BINA_Q_search_api/serializers/search_serializers.py
from rest_framework import serializers
from BINA_Q_healthcare_workers.models import HealthcareWorker
from BINA_Q_users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class HealthcareWorkerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = HealthcareWorker
        fields = [
            "user",
            "identifier",
            "license_number",
            "specialization",
            "organisation_affiliation",
            "ods_code",
        ]
