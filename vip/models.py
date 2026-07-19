from django.db import models

class SiteConfig(models.Model):
    capacity = models.PositiveIntegerField(default=10, verbose_name="ظرفیت")
    is_open = models.BooleanField(default=True, verbose_name="ثبت‌نام فعال باشد؟")
    closed_message = models.CharField(
        max_length=200,
        default="ظرفیت این دوره تکمیل شده است.",
        verbose_name="پیام تکمیل ظرفیت"
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "VIP Config"

    @staticmethod
    def get():
        obj = SiteConfig.objects.first()
        if not obj:
            obj = SiteConfig.objects.create(capacity=10, is_open=True)
        return obj

    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات سایت"


class Submission(models.Model):
    full_name = models.CharField(max_length=80, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=20, verbose_name="شماره تماس")
    receipt = models.ImageField(upload_to="receipts/", verbose_name="عکس رسید")
    note = models.CharField(max_length=300, blank=True, verbose_name="توضیحات (اختیاری)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.phone}"

    class Meta:
        verbose_name = "ارسال اطلاعات"
        verbose_name_plural = "ارسال‌های کاربران"
        ordering = ["-created_at"]