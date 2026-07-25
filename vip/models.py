from django.db import models

class SiteConfig(models.Model):
    capacity = models.PositiveIntegerField(default=10, verbose_name="ظرفیت")
    is_open = models.BooleanField(default=True, verbose_name="ثبت‌نام فعال باشد؟")
    closed_message = models.CharField(
        max_length=200,
        default="ظرفیت این پلن تکمیل شده است.",
        verbose_name="پیام تکمیل ظرفیت"
    )
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
            obj = SiteConfig.objects.create(capacity=10, is_open=True)
        return obj


class Submission(models.Model):
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