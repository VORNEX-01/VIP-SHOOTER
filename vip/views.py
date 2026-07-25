from django.shortcuts import render, redirect
from django.utils import timezone
from .models import SiteConfig, Submission, InviteLink
from .forms import SubmissionForm

CARD_NUMBER = "6219861996348339"
CARD_OWNER = "محمد فریدونی"

PLAN_PRICE = "19 میلیون و 800 هزار تومان"

PLAN_BULLETS = [
    "محتواهاتو اصولی و برمبنای تفکر درست میسازی",
    "عاشق محتوا ساختن میشی و همچنین مسیر درامدزایی رو واسه خودت میچینی.",
    "اهدافت رو درست انتخاب میکنی و در طول مسیر خودم شخصا کنارتم که به بهترین شکل پیجت رو شخصی سازی کنی!",
    "اینجا قصد بر اینه که شما بعد از یک ماه به فرآیند های پیجتون مسلط بشین و بدون وابستگی بر اساس ذهنیت درست فعالیتتون رو ادامه بدین.",
    "فعالیت با سبکی که دوستش دارید ، قسمتی از لایف استایل شماست و در وجود شما بعد از این یک ماه نهادینه میشه.",
    "دقت کن که VIP SHOOTER یک پلن آموزشی ویدیو محور نیست، یک پلن یکماهه‌ست که روی اصلاح روند و رفع اشکال حین فعالیت شما به صورت فشرده تمرکز داره.",
    "میخوایم خود واقعیتو با اصول درست محتوایی ترکیب کنیم نه صرفا محتوا بسازیم.",
    "باید اینو بدونی که من اونیم که مسیر رو بهت نشون میده و تو اونی هستی که باید با تلاشت ورق رو برگردونی.",
    "در نهایت باید بدونی که این دوره برای افراد مصمم طراحی شده و در صورت عدم تلاش یا عدم عملی کردن مسیر اجرایی ،هیچگونه کمکی از من برای رشد پیج شما برنخواهد آمد و مسئولیتی بابت عدم اراده شما نخواهم پذیرفت.",
]

def home(request, token=None):
    cfg = SiteConfig.get()

    used = Submission.objects.count()
    is_full = (used >= cfg.capacity) or (not cfg.is_open)

    sent = request.GET.get("sent") == "1"
    already = request.GET.get("already") == "1"

    invite_status = "ok"
    invite_obj = None

    # گیت لینک اختصاصی
    if token is not None:
        try:
            invite_obj = InviteLink.objects.get(token=token)
        except InviteLink.DoesNotExist:
            invite_status = "invalid"
        else:
            if invite_obj.is_used:
                invite_status = "used"
            elif invite_obj.is_expired:
                invite_status = "expired"
            else:
                invite_status = "ok"
    else:
        # اگر بخوای سایت فقط با لینک کار کنه اینو فعال کن:
        invite_status = "missing"

    locked = is_full or (invite_status in ["missing", "invalid", "expired", "used"])

    if request.method == "POST":
        if locked:
            return redirect(request.path + "?full=1" if is_full else request.path + "?expired=1")

        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            phone = form.cleaned_data["phone"].strip()

            if Submission.objects.filter(phone=phone).exists():
                return redirect(request.path + "?already=1")

            obj = form.save(commit=False)
            obj.invite = invite_obj
            obj.save()

            # لینک مصرف شود
            if invite_obj:
                invite_obj.is_used = True
                invite_obj.used_at = timezone.now()
                invite_obj.save(update_fields=["is_used", "used_at"])

            request.session["last_full_name"] = obj.full_name
            return redirect(request.path + "?sent=1")
    else:
        form = SubmissionForm()

    show_full = (request.GET.get("full") == "1") or is_full
    show_expired = (request.GET.get("expired") == "1") or (invite_status in ["missing", "invalid", "expired", "used"])

    last_name = request.session.get("last_full_name", "")

    return render(request, "vip/home.html", {
        "form": form,
        "sent": sent,
        "already": already,

        "is_full": is_full,
        "show_full": show_full,
        "closed_message": cfg.closed_message,

        "invite_status": invite_status,
        "show_expired": show_expired,

        "card_number": CARD_NUMBER,
        "card_owner": CARD_OWNER,

        "telegram_id": cfg.telegram_id,
        "instagram_url": cfg.instagram_url,
        "telegram_shooter_vip": cfg.telegram_shooter_vip,

        "plan_price": PLAN_PRICE,
        "plan_bullets": PLAN_BULLETS,
        "last_name": last_name,
        "locked": locked,
    })