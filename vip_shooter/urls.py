import os
from django.contrib import admin
from django.urls import path, include

ADMIN_PATH = os.environ.get("ADMIN_PATH", "01-control-vipshooter").strip("/")

urlpatterns = [
    path("", include("vip.urls")),
    path(f"{ADMIN_PATH}/", admin.site.urls),
]