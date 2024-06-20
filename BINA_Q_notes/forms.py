# BINA_Q_notes/forms.py
from django import forms
from .models import Note, NoteResponse


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


class NoteResponseForm(forms.ModelForm):
    class Meta:
        model = NoteResponse
        fields = ("response",)
