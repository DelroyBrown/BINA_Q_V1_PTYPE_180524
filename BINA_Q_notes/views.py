# BINA_Q_notes/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Note
from .forms import NoteForm, NoteResponseForm


@login_required
def note_list(request):
    notes = Note.objects.filter(author=request.user) | Note.objects.filter(
        tags=request.user
    )
    notes = notes.distinct().order_by("-created_at")
    return render(request, "notes/note_list.html", {"notes": notes})


@login_required
def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    responses = note.note_responses.all()
    if note.author != request.user:
        return render(request, "notes/note_not_allowed.html")
    if request.method == "POST":
        form = NoteResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.author = request.user
            response.note = note
            response.save()
            return redirect("BINA_Q_notes:note_detail", note_id=note_id)
    return render(
        request, "notes/note_detail.html", {"note": note, "responses": responses}
    )


@login_required
def note_create(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            form.save_m2m()  # this saves the tags
            return redirect("BINA_Q_notes:note_list")
    else:
        form = NoteForm()
    return render(request, "notes/note_form.html", {"form": form})


def note_edit(request, note_id):
    note = get_object_or_404(Note, id=note_id, author=request.user)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect("BINA_Q_notes:note_list")
    else:
        form = NoteForm(instance=note)
    return render(request, "notes/note_form.html", {"form": form})


@login_required
def note_delete(request, note_id):
    note = get_object_or_404(Note, id=note_id, author=request.user)
    if request.method == "POST":
        note.delete()
        return redirect("BINA_Q_notes:note_list")
    return render(request, "notes/note_confirm_delete.html", {"note": note})


@login_required
def note_response_create(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == "POST":
        form = NoteResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.author = request.user
            response.note = note
            response.save()
            return redirect("BINA_Q_notes:note_detail", note_id=note_id)
    else:
        form = NoteResponseForm()
    return render(request, "notes/note_comment_form.html", {"form": form, "note": note})
