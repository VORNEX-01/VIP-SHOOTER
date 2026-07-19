# vip/views.py
from django.shortcuts import render, redirect
from .models import SiteConfig, Submission
from .forms import SubmissionForm

def home(request):
    cfg = SiteConfig.get()
    used = Submission.objects.count()
    is_full = (used >= cfg.capacity) or (not cfg.is_open)

    sent = request.GET.get("sent") == "1"
    already = request.GET.get("already") == "1"

    if request.method == "POST":
        if is_full:
            return redirect("/?full=1")

        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            phone = form.cleaned_data["phone"].strip()

            # جلوگیری از تکراری
            if Submission.objects.filter(phone=phone).exists():
                return redirect("/?already=1")

            form.save()
            return redirect("/?sent=1")
    else:
        form = SubmissionForm()

    show_full = (request.GET.get("full") == "1") or is_full

    return render(request, "vip/home.html", {
        "form": form,
        "sent": sent,
        "already": already,
        "is_full": is_full,
        "show_full": show_full,
        "closed_message": cfg.closed_message,
        "capacity": cfg.capacity,
        "used": used,
        "card_number": "6219861996348339",
        "card_owner": "محمد فریدونی",
        "telegram_id": "Mohamadfereidouny",
        "instagram_url": "https://www.instagram.com/mohamadfereidouny?igsh=dHFmNnVmZzdwbHA=",
    })