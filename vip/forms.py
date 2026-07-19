# vip/forms.py
from django import forms
from .models import Submission

MAX_RECEIPT_MB = 3

class SubmissionForm(forms.ModelForm):
    ready = forms.BooleanField(required=True, label="آماده‌ام")

    class Meta:
        model = Submission
        fields = ["full_name", "phone", "note", "receipt"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class":"input", "placeholder":"نام و نام خانوادگی"}),
            "phone": forms.TextInput(attrs={"class":"input", "placeholder":"شماره تماس", "inputmode":"tel"}),
            "note": forms.TextInput(attrs={"class":"input", "placeholder":"توضیحات (اختیاری)"}),
        }

    receipt = forms.ImageField(required=True, widget=forms.ClearableFileInput(attrs={
        "class":"file",
        "accept":"image/*"
    }))

    def clean_receipt(self):
        f = self.cleaned_data.get("receipt")
        if not f:
            return f
        limit = MAX_RECEIPT_MB * 1024 * 1024
        if f.size > limit:
            raise forms.ValidationError(f"حجم عکس رسید نباید بیشتر از {MAX_RECEIPT_MB}MB باشد.")
        return f