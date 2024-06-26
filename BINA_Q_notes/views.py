# BINA_Q_notes/views.py
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Note, Notification
from BINA_Q_users.models import User
from .forms import NoteForm, NoteResponseForm


@login_required
def note_list(request):
    notes = Note.objects.filter(author=request.user) | Note.objects.filter(
        tags=request.user
    )
    notes = notes.distinct().order_by("-created_at")

    notes_with_responses = [(note, note.note_responses.all()) for note in notes]

    return render(
        request, "notes/note_list.html", {"notes_with_responses": notes_with_responses}
    )


@login_required
def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    responses = note.note_responses.all()

    if request.user != note.author and request.user not in note.tags.all():
        return render(request, "notes/note_not_allowed.html")

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

    return render(
        request,
        "notes/note_detail.html",
        {"note": note, "responses": responses, "form": form},
    )


@login_required
def note_create(request):
    if request.method == "POST":
        form = NoteForm(request.POST, user=request.user)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            form.save_m2m()  # this saves the tags
            return redirect("BINA_Q_notes:note_list")
    else:
        form = NoteForm(user=request.user)
    return render(request, "notes/note_form.html", {"form": form})


@login_required
def note_edit(request, note_id):
    note = get_object_or_404(Note, id=note_id, author=request.user)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("BINA_Q_notes:note_list")
    else:
        form = NoteForm(instance=note, user=request.user)
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


@login_required
def note_create_with_tag(request, user_id):
    tagged_user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = NoteForm(request.POST, user=request.user)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            note.tags.add(tagged_user)
            form.save_m2m()

            message = f"You have been tagged in the note '{note.title}'"
            notification = Notification.objects.create(
                user=tagged_user, note=note, message=message
            )
            print(
                f"Notification created: {notification}"
            )

            return redirect("BINA_Q_notes:note_list")
    else:
        form = NoteForm(user=request.user)
        form.fields["tags"].initial = [tagged_user]

    return render(request, "notes/note_form.html", {"form": form})


@login_required
def tagged_notes(request):
    tagged_notes = Note.objects.filter(tags=request.user).order_by("-created_at")
    return render(request, "notes/tagged_notes.html", {"tagged_notes": tagged_notes})


def fetch_notifications(request):
    notifications = Notification.objects.filter(
        user=request.user, is_read=False
    ).order_by("-created_at")
    data = [
        {"id": n.id, "message": n.message, "note_id": n.note.id} for n in notifications
    ]
    return JsonResponse(data, safe=False)
