from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import SiteConfig, Submission, InviteLink

admin.site.site_header = "پنل مدیریت VIP SHOOTER"
admin.site.site_title = "VIP SHOOTER Admin"
admin.site.index_title = "مدیریت سایت"

@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ("capacity", "is_open", "default_link_minutes", "updated_at")
    fields = ("capacity", "is_open", "closed_message", "default_link_minutes", "telegram_id", "instagram_url", "telegram_shooter_vip")

@admin.register(InviteLink)
class InviteLinkAdmin(admin.ModelAdmin):
    list_display = ("token", "minutes", "expires_at", "is_used", "created_at", "link_path")
    list_filter = ("is_used", "created_at")
    search_fields = ("token",)
    readonly_fields = ("token", "created_at", "link_path")
    fields = ("token", "minutes", "expires_at", "is_used", "used_at", "created_at", "link_path")

    def link_path(self, obj):
        # لینک نسبی؛ دامنه رو خودت می‌چسبونی
        return format_html('<code>https://vip-shooter.up.railway.app/user/{}/</code>', obj.token)
    link_path.short_description = "لینک"

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "national_id", "created_at", "invite", "receipt_thumb")
    search_fields = ("full_name", "phone", "national_id", "invite__token")
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "receipt_preview")

    fieldsets = (
        ("اطلاعات کاربر", {"fields": ("full_name", "phone", "national_id", "invite", "created_at")}),
        ("رسید پرداخت", {"fields": ("receipt", "receipt_preview")}),
    )

    def receipt_thumb(self, obj):
        if not obj.receipt:
            return "-"
        try:
            url = obj.receipt.url
        except Exception:
            return "فایل موجود نیست"
        return format_html(
            '<a href="{0}" target="_blank">'
            '<img src="{0}" style="height:44px;width:44px;object-fit:cover;border-radius:10px;border:1px solid #ddd" />'
            "</a>",
            url,
        )
    receipt_thumb.short_description = "رسید"

    def receipt_preview(self, obj):
        if not obj.receipt:
            return "-"
        try:
            url = obj.receipt.url
        except Exception:
            return "فایل موجود نیست"
        return format_html(
            '<a href="{0}" target="_blank" style="display:inline-block">'
            '<img src="{0}" style="max-height:360px;max-width:100%;border-radius:14px;border:1px solid #ddd" />'
            "</a>",
            url
        )
    receipt_preview.short_description = "پیش‌نمایش"