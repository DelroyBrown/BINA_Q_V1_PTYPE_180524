from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from .views import home
from django.urls import path, include

app_name = "BINA_Q_base"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("healthcare-workers/", include("BINA_Q_healthcare_workers.urls")),
    path("organisations/", include("BINA_Q_organisations.urls")),
    path("pharmacies/", include("BINA_Q_pharmacies.urls")),
    path("roles/", include("BINA_Q_roles.urls")),
    path("users/", include("BINA_Q_users.urls")),
    path("notes/", include("BINA_Q_notes.urls")),
    path("search/", include("BINA_Q_search_api.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
