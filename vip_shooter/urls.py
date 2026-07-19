import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

ADMIN_PATH = os.environ.get("ADMIN_PATH", "01-control-vipshooter").strip("/")

urlpatterns = [
    path("", include("vip.urls")),
    path(f"{ADMIN_PATH}/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)