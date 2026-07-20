from django.contrib import admin
from django.utils.html import format_html
from .models import SiteConfig, Submission

admin.site.site_header = "پنل مدیریت VIP SHOOTER"
admin.site.site_title = "VIP SHOOTER Admin"
admin.site.index_title = "مدیریت سایت"

@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ("capacity", "is_open", "updated_at")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "created_at", "receipt_thumb")
    search_fields = ("full_name", "phone")
    list_filter = ("created_at",)
    readonly_fields = ("receipt_preview",)

    fieldsets = (
        ("اطلاعات کاربر", {"fields": ("full_name", "phone", "note", "created_at")}),
        ("رسید پرداخت", {"fields": ("receipt", "receipt_preview")}),
    )

    def receipt_thumb(self, obj):
        if obj.receipt:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="height:44px;width:44px;object-fit:cover;border-radius:10px;border:1px solid #ddd" /></a>',
                obj.receipt.url, obj.receipt.url
            )
        return "-"
    receipt_thumb.short_description = "رسید"

    def receipt_preview(self, obj):
        if obj.receipt:
            return format_html(
                '<a href="{0}" target="_blank" style="display:inline-block">'
                '<img src="{0}" style="max-height:360px;max-width:100%;border-radius:14px;border:1px solid #ddd" />'
                "</a>",
                obj.receipt.url
            )
        return "-"
    receipt_preview.short_description = "پیش‌نمایش"