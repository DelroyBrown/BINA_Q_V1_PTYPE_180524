# BINA_Q_notes/forms.py
from django import forms
from .models import Note, NoteResponse
from BINA_Q_healthcare_workers.models import HealthcareWorker
from BINA_Q_users.models import User

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = [
            "title",
            "content",
            "importance",
            "reminder",
            "tags",
        ]
        widgets = {
            "reminder": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(NoteForm, self).__init__(*args, **kwargs)
        if user:
            healthcare_worker = HealthcareWorker.objects.get(user=user)
            self.fields["tags"].queryset = User.objects.filter(
                healthcareworker__organisation_affiliation=healthcare_worker.organisation_affiliation
            )


class NoteResponseForm(forms.ModelForm):
    class Meta:
        model = NoteResponse
        fields = ("response",)
