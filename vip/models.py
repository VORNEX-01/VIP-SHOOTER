import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta

class SiteConfig(models.Model):
    capacity = models.PositiveIntegerField(default=10, verbose_name="ظرفیت")
    is_open = models.BooleanField(default=True, verbose_name="ثبت‌نام فعال باشد؟")
    closed_message = models.CharField(
        max_length=200,
        default="ظرفیت این پلن تکمیل شده است.",
        verbose_name="پیام تکمیل ظرفیت"
    )

    # Socials (قابل مدیریت در ادمین)
    telegram_id = models.CharField(max_length=60, default="Mohamadfereidouny", verbose_name="آیدی تلگرام محمد فریدونی")
    instagram_url = models.URLField(
        max_length=300,
        default="https://www.instagram.com/mohamadfereidouny?igsh=dHFmNnVmZzdwbHA=",
        verbose_name="لینک اینستاگرام"
    )
    telegram_shooter_vip = models.CharField(max_length=60, default="SHOOTER_VIP", verbose_name="آیدی تلگرام SHOOTER_VIP")

    # Default link validity
    default_link_minutes = models.PositiveIntegerField(default=20, verbose_name="اعتبار پیش‌فرض لینک (دقیقه)")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین تغییر")

    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات سایت"

    def __str__(self):
        return "تنظیمات سایت"

    @staticmethod
    def get():
        obj = SiteConfig.objects.first()
        if not obj:
            obj = SiteConfig.objects.create()
        return obj


class InviteLink(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, verbose_name="توکن")
    minutes = models.PositiveIntegerField(default=20, verbose_name="اعتبار (دقیقه)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ساخت")
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان انقضا")
    is_used = models.BooleanField(default=False, verbose_name="استفاده شده؟")
    used_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان استفاده")

    class Meta:
        verbose_name = "لینک اختصاصی"
        verbose_name_plural = "لینک‌های اختصاصی"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=self.minutes)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() >= (self.expires_at or timezone.now())

    def __str__(self):
        return str(self.token)


class Submission(models.Model):
    invite = models.ForeignKey(InviteLink, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="لینک اختصاصی")
    full_name = models.CharField(max_length=80, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=20, verbose_name="شماره تماس")
    national_id = models.CharField(max_length=20, verbose_name="کد ملی")
    receipt = models.ImageField(upload_to="receipts/", verbose_name="عکس رسید")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ثبت")

    class Meta:
        verbose_name = "ارسال اطلاعات"
        verbose_name_plural = "ارسال‌های کاربران"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.phone}"