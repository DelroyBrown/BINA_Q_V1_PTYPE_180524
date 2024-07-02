# BINA_Q_notes/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    note_list,
    note_delete,
    note_detail,
    note_create,
    note_edit,
    note_response_create,
    note_create_with_tag,
    tagged_notes,
    fetch_notifications,
)

app_name = "BINA_Q_notes"

urlpatterns = [
    path("", note_list, name="note_list"),
    path("<int:note_id>/", note_detail, name="note_detail"),
    path("new/", note_create, name="note_create"),
    path("<int:note_id>/response/", note_response_create, name="note_response_create"),
    path("<int:note_id>/edit/", note_edit, name="note_edit"),
    path("<int:note_id>/delete/", note_delete, name="note_delete"),
    path("new/<int:user_id>/", note_create_with_tag, name="note_create_with_tag"),
    path("tagged/", tagged_notes, name="tagged_notes"),
    path("notifications/", fetch_notifications, name="fetch_notifications"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
