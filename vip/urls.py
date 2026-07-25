from django.urls import path
from .views import home

urlpatterns = [
    path("", home, name="home"),                    # اگر خواستی عمومی بمونه
    path("user/<uuid:token>/", home, name="invite"),   # لینک اختصاصی
]