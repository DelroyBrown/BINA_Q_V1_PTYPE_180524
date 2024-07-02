# BINA_Q_search_api/serializers/search_serializers.py
from rest_framework import serializers
from BINA_Q_healthcare_workers.models import HealthcareWorker
from BINA_Q_users.models import User
import json

with open("BINA_Q_healthcare_workers/fixtures/ods_codes.json") as f:
    ODS_CODES = json.load(f)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class HealthcareWorkerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    ods_code_info = serializers.SerializerMethodField()

    class Meta:
        model = HealthcareWorker
        fields = [
            "user",
            "identifier",
            "license_number",
            "specialization",
            "organisation_affiliation",
            "ods_code",
            "ods_code_info",
        ]

    def get_ods_code_info(self, obj):
        ods_code = obj.ods_code
        ods_info = next(
            (item for item in ODS_CODES["ods_codes"] if item["ods_code"] == ods_code),
            None,
        )
        return ods_info
