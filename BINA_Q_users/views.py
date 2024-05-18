import json
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from BINA_Q_healthcare_workers.models import HealthcareWorker
from .forms import LoginForm, PasswordChangeForm, DashboardUpdateForm, ODSCodeUpdateForm


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            bina_q_id = form.cleaned_data["bina_q_id"]
            password = form.cleaned_data["password"]
            user = authenticate(request, bina_q_id=bina_q_id, password=password)
            if user is not None:
                login(request, user)
                return redirect("BINA_Q_users:check_temporary_password")
            else:
                form.add_error(None, "Invalid BINA-Q ID or password.")
    else:
        form = LoginForm()
    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("BINA_Q_users:login")


def logout_confirmation_view(request):
    return render(request, "registration/logout_confirmation.html")


def password_change_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data["new_password1"]
            user = request.user
            user.set_password(new_password)
            user.is_temporary_password = False
            user.save()
            update_session_auth_hash(request, user)
            return redirect("BINA_Q_healthcare_workers:dashboard")
    else:
        form = PasswordChangeForm()
    return render(request, "registration/password_change.html", {"form": form})


@login_required
def check_temporary_password(request):
    if request.user.is_temporary_password:
        return redirect("BINA_Q_users:password_change")
    return redirect("BINA_Q_healthcare_workers:dashboard")


from django.http import JsonResponse


@login_required
def dashboard_update_view(request):
    user = request.user
    try:
        healthcare_worker = HealthcareWorker.objects.get(user=user)
    except HealthcareWorker.DoesNotExist:
        healthcare_worker = None

    if request.method == "POST":
        profile_form = DashboardUpdateForm(request.POST, instance=user)
        ods_form = ODSCodeUpdateForm(request.POST, instance=healthcare_worker)
        if profile_form.is_valid() and ods_form.is_valid():
            profile_form.save()
            ods_form.save()
            return redirect("BINA_Q_healthcare_workers:dashboard")
    else:
        profile_form = DashboardUpdateForm(instance=user)
        ods_form = ODSCodeUpdateForm(instance=healthcare_worker)

    context = {
        "profile_form": profile_form,
        "ods_form": ods_form,
    }
    return render(request, "dashboard/dashboard_update.html", context)


def fetch_ods_details(request):
    ods_code = request.GET.get("ods_code")
    if not ods_code:
        return JsonResponse({"error": "ODS Code is required!"}, status=400)

    with open(
        settings.BASE_DIR / "BINA_Q_healthcare_workers/fixtures/ods_codes.json"
    ) as f:
        ods_codes_data = json.load(f)

    organisation_details = next(
        (ods for ods in ods_codes_data["ods_codes"] if ods["ods_code"] == ods_code),
        None,
    )

    if not organisation_details:
        return JsonResponse({"error": "ODS Code not found."}, status=400)

    return JsonResponse({"organisation_details": organisation_details})
