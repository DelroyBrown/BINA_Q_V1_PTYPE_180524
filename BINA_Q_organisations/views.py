# BINA_Q_organisations/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from BINA_Q_healthcare_workers.models import HealthcareWorker


@login_required
def organisation_members(request):
    user = request.user
    try:
        healthcare_worker = HealthcareWorker.objects.get(user=user)
        organisation_affiliation = healthcare_worker.organisation_affiliation
        # Filter by organisation affiliation and exclude the logged-in user
        organisation_members = HealthcareWorker.objects.filter(
            organisation_affiliation=organisation_affiliation
        ).exclude(user=user)
    except HealthcareWorker.DoesNotExist:
        organisation_members = []

    return render(
        request,
        "organisations/members.html",
        {"organisation_members": organisation_members},
    )
