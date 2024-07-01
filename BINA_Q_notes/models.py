# BINA_Q_notes/models.py
from django.db import models
from django.conf import settings


class Note(models.Model):
    URGENCY_LEVEL = [
        (1, "1 - Low"),
        (2, "2"),
        (3, "3 - Medium"),
        (4, "4"),
        (5, "5 - High"),
    ]
    title = models.CharField(max_length=100, blank=False, null=False, default="")
    content = models.TextField(max_length=5000, blank=False, null=False, default="")
    importance = models.IntegerField(choices=URGENCY_LEVEL, default="3 - Medium")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reminder = models.DateTimeField(null=True, blank=True)
    tags = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="tagged_notes"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="notes", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class NoteResponse(models.Model):
    note = models.ForeignKey(
        Note, on_delete=models.CASCADE, related_name="note_responses"
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    response = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to {self.note.title} by {self.author.get_username()}"


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="notifications", on_delete=models.CASCADE
    )
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.get_full_name()} about {self.note.title}"
