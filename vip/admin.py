from django.contrib import admin
from .models import SiteConfig, Submission

admin.site.site_header = "پنل مدیریت VIP SHOOTER"
admin.site.site_title = "VIP SHOOTER Admin"
admin.site.index_title = "مدیریت سایت"

@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ("capacity", "is_open", "updated_at")

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "created_at")
    search_fields = ("full_name", "phone")
    list_filter = ("created_at",)