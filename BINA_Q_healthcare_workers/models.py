from django.db import models
import random
import string
from django.conf import settings


class HealthcareWorker(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=50, unique=True)
    license_number = models.CharField(max_length=50)
    specialization = models.CharField(max_length=100)
    organisation_affiliation = models.CharField(max_length=100)
    ods_code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.identifier}"
