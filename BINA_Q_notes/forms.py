from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = [
            'title',
            'content',
            'importance',
            'reminder',
            'tags',
        ]
        widgets = {
            'reminder' : forms.DateTimeInput(attrs={'type' : 'datetime-local'}),
            'tags' : forms.SelectMultiple(attrs={'class' : 'form-control'}),
        }

