from django.shortcuts import render, redirect
from .models import SiteConfig, Submission
from .forms import SubmissionForm

CARD_NUMBER = "6219861996348339"
CARD_OWNER = "محمد فریدونی"

TELEGRAM_ID_PERSONAL = "Mohamadfereidouny"
INSTAGRAM_URL_PERSONAL = "https://www.instagram.com/mohamadfereidouny?igsh=dHFmNnVmZzdwbHA="
TELEGRAM_SHOOTER_VIP = "SHOOTER_VIP"

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

def home(request):
    cfg = SiteConfig.get()
    used = Submission.objects.count()
    is_full = (used >= cfg.capacity) or (not cfg.is_open)

    sent = request.GET.get("sent") == "1"
    already = request.GET.get("already") == "1"
    show_full = (request.GET.get("full") == "1") or is_full

    last_name = request.session.get("last_full_name", "")

    if request.method == "POST":
        if is_full:
            return redirect("/?full=1")

        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            phone = form.cleaned_data["phone"].strip()

            if Submission.objects.filter(phone=phone).exists():
                return redirect("/?already=1")

            obj = form.save()
            request.session["last_full_name"] = obj.full_name
            return redirect("/?sent=1")
    else:
        form = SubmissionForm()

    return render(request, "vip/home.html", {
        "form": form,
        "sent": sent,
        "already": already,
        "is_full": is_full,
        "show_full": show_full,
        "closed_message": cfg.closed_message,
        "capacity": cfg.capacity,
        "used": used,

        "card_number": CARD_NUMBER,
        "card_owner": CARD_OWNER,

        "telegram_id": TELEGRAM_ID_PERSONAL,
        "instagram_url": INSTAGRAM_URL_PERSONAL,

        "telegram_shooter_vip": TELEGRAM_SHOOTER_VIP,
        "plan_price": PLAN_PRICE,
        "plan_bullets": PLAN_BULLETS,
        "last_name": last_name,
    })