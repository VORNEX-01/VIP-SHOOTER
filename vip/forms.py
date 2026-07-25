from django import forms
from .models import Submission

MAX_RECEIPT_MB = 3

class SubmissionForm(forms.ModelForm):
    accept = forms.BooleanField(required=True, label="شرایط پلن رو خواندم و می‌پذیرم")

    class Meta:
        model = Submission
        fields = ["full_name", "phone", "national_id", "receipt"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class":"input", "placeholder":"نام و نام خانوادگی"}),
            "phone": forms.TextInput(attrs={"class":"input", "placeholder":"شماره تماس (ضروری)", "inputmode":"tel"}),
            "national_id": forms.TextInput(attrs={"class":"input", "placeholder":"کد ملی (ضروری)", "inputmode":"numeric"}),
        }

    receipt = forms.ImageField(required=True, widget=forms.ClearableFileInput(attrs={
        "class":"file",
        "accept":"image/*",
    }))

    def clean_receipt(self):
        f = self.cleaned_data.get("receipt")
        if not f:
            return f
        limit = MAX_RECEIPT_MB * 1024 * 1024
        if f.size > limit:
            raise forms.ValidationError(f"حجم عکس رسید نباید بیشتر از {MAX_RECEIPT_MB}MB باشد.")
        return f