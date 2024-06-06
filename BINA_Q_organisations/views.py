from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from BINA_Q_healthcare_workers.models import HealthcareWorker


@login_required
def organisation_members(request):
    user = request.user
    try:
        healthcare_worker = HealthcareWorker.objects.get(user=user)
        ods_code = healthcare_worker.ods_code
        organisation_memebers = HealthcareWorker.objects.filter(ods_code=ods_code)
    except HealthcareWorker.DoesNotExist:
        organisation_memebers = []

    return render(
        request,
        "organisations/members.html",
        {"organisation_members": organisation_memebers},
    )
