# BINA_Q_healthcare_workers/views.py
import json
import random
import string
from django.db import IntegrityError
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from .forms import ProfessionalIdentifierForm
from .models import HealthcareWorker
from BINA_Q_users.models import User


def register(request):
    if request.method == "POST":
        form = ProfessionalIdentifierForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data["identifier"]
            email = form.cleaned_data["email"]
            # Then i've stored the identifier and email in the session for later use
            request.session["identifier"] = identifier
            request.session["email"] = email
            return redirect(reverse("BINA_Q_healthcare_workers:retrieve_data"))
    else:
        form = ProfessionalIdentifierForm()
    return render(request, "registration/register.html", {"form": form})


class ConfirmationForm(forms.Form):
    identifier = forms.CharField(max_length=50, required=True)
    first_name = forms.CharField(max_length=250, required=True)
    last_name = forms.CharField(max_length=250, required=True)
    license_number = forms.CharField(max_length=50, required=True)
    specialization = forms.CharField(max_length=100, required=True)
    organisation_affiliation = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=255, required=True)
    ods_code = forms.CharField(max_length=50, required=True)
    organisation_name = forms.CharField(max_length=255, required=True)
    address = forms.CharField(max_length=500, required=True)
    contact_number = forms.CharField(max_length=50, required=True)


def confirm_data(request):
    combined_data = request.session.get("combined_data")

    if not combined_data:
        return redirect("register")

    if request.method == "POST":
        form = ConfirmationForm(request.POST)
        if form.is_valid():
            # Here's where i save the confirmed data in the session
            request.session["confirmed_data"] = form.cleaned_data
            return redirect("BINA_Q_healthcare_workers:complete_registration")
    else:
        form = ConfirmationForm(initial=combined_data)
    return render(request, "registration/confirm.html", {"form": form})


def retrieve_data(request):
    identifier = request.session.get("identifier")
    email = request.session.get("email")

    if not identifier or not email:
        return redirect("BINA_healthcare_workers:register")

    with open(
        settings.BASE_DIR / "BINA_Q_healthcare_workers/fixtures/healthcare_workers.json"
    ) as f:
        healthcare_workers = json.load(f)

    healthcare_worker_data = next(
        (
            worker
            for worker in healthcare_workers["healthcare_workers"]
            if worker["identifier"] == identifier
        ),
        None,
    )

    if not healthcare_worker_data:
        return render(
            request,
            "registration/commons/error.html",
            {"message": "Healthcare worker not found!"},
        )

    with open(
        settings.BASE_DIR / "BINA_Q_healthcare_workers/fixtures/ods_codes.json"
    ) as f:
        ods_codes = json.load(f)

    ods_data = next(
        (
            ods
            for ods in ods_codes["ods_codes"]
            if ods["ods_code"] == healthcare_worker_data["ods_code"]
        ),
        None,
    )

    if not ods_data:
        return render(
            request,
            "registration/commons/error.html",
            {"message": "ODS Code not found!"},
        )

    combined_data = {
        "identifier": healthcare_worker_data["identifier"],
        "first_name": healthcare_worker_data["first_name"],
        "last_name": healthcare_worker_data["last_name"],
        "license_number": healthcare_worker_data["license_number"],
        "specialization": healthcare_worker_data["specialization"],
        "organisation_affiliation": healthcare_worker_data["organisation_affiliation"],
        "email": email,
        "ods_code": healthcare_worker_data["ods_code"],
        "organisation_name": ods_data["organisation_name"],
        "address": ods_data["address"],
        "contact_number": ods_data["contact_number"],
    }

    if request.method == "POST":
        form = ConfirmationForm(request.POST)
        if form.is_valid():
            request.session["confirmed_data"] = form.cleaned_data
            return redirect("BINA_Q_healthcare_workers:complete_registration")
    else:
        form = ConfirmationForm(initial=combined_data)

    return render(request, "registration/retrieve.html", {"form": form})


def generate_temp_password():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=8))


def generate_bina_q_id(first_name, last_name):
    random_chars = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{first_name[:3].upper()}{last_name[:3].upper()}-{random_chars}"


def complete_registration(request):
    confirmed_data = request.session.get("confirmed_data")

    if not confirmed_data:
        return redirect("BINA_Q_healthcare_workers:register")

    email = confirmed_data["email"]
    user = User.objects.filter(email=email).first()

    if user:
        return render(
            request,
            "registration/commons/error.html",
            {"message": f"A user with the email {email} already exists."},
        )
    else:
        bina_q_id = generate_bina_q_id(
            confirmed_data["first_name"], confirmed_data["last_name"]
        )

        temp_password = generate_temp_password()

        # Create the User record
        user = User(
            email=email,
            password=make_password(temp_password),
            bina_q_id=bina_q_id,
            first_name=confirmed_data["first_name"],
            last_name=confirmed_data["last_name"],
        )
        user.save()

        # Add a debugging statement to ensure the user is saved
        print(f"User created with ID: {user.id}")

        try:
            # Create the Healthcare Worker record
            healthcare_worker = HealthcareWorker(
                user=user,
                identifier=confirmed_data["identifier"],
                license_number=confirmed_data["license_number"],
                specialization=confirmed_data["specialization"],
                organisation_affiliation=confirmed_data["organisation_affiliation"],
                ods_code=confirmed_data["ods_code"],
            )
            healthcare_worker.save()

            # Add a debugging statement to ensure the healthcare worker is saved
            print(f"Healthcare worker created with ID: {healthcare_worker.id}")

            # Send the email to the user
            send_mail(
                "Your BINA-Q Registration",
                f"Hello {confirmed_data['first_name']}, \n\nYour BINA-Q ID is {bina_q_id}.\nYour temporary password is {temp_password}. Please log in and change your password.\n\nThank you!",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            return redirect("BINA_Q_healthcare_workers:registration_success")

        except IntegrityError as e:
            # If there's an integrity error, it likely means the identifier is not unique
            if "UNIQUE constraint" in str(e):
                return render(
                    request,
                    "registration/commons/error.html",
                    {
                        "message": f"A healthcare worker with the identifier {confirmed_data['identifier']} already exists."
                    },
                )
            else:
                raise e


def registration_success(request):
    return render(request, "registration/registration_success.html")


@login_required
def dashboard_view(request):
    user = request.user
    try:
        healthcare_worker = HealthcareWorker.objects.get(user=user)
    except HealthcareWorker.DoesNotExist:
        healthcare_worker = None

    organisation_details = {}

    if healthcare_worker:
        ods_code = healthcare_worker.ods_code
        # Here's where I load the ODS data from the JSON file
        with open("BINA_Q_healthcare_workers/fixtures/ods_codes.json") as f:
            ods_codes_data = json.load(f)

        # Find the matching ODS code in the list
        ods_codes_list = ods_codes_data.get("ods_codes", [])
        for entry in ods_codes_list:
            if entry["ods_code"] == ods_code:
                organisation_details = entry
                break

    context = {
        "user": user,
        "healthcare_worker": healthcare_worker,
        "organisation_details": organisation_details,
    }

    return render(request, "dashboard/dashboard.html", context)


