import os
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

ADMIN_PATH = os.environ.get("ADMIN_PATH", "01-control-vipshooter").strip("/")

urlpatterns = [
    path("", include("vip.urls")),
    path(f"{ADMIN_PATH}/", admin.site.urls),

    # Serve MEDIA in production too (Railway)
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]