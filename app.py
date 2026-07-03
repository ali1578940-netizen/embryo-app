import os
import json
import random
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
app.secret_key = "embryo_pro_2026"

# =========================================================
# ۱. داده‌های آموزشی (خلاصه فشرده ولی کامل)
# =========================================================
summary_content = """
<h2>۱. بلوغ تخمک و اسپرم</h2>
<p><strong>تخمک:</strong> در فولیکول اولیه در پروفاز میوز I است. افزایش ناگهانی LH قبل از تخمک‌گذاری، میوز I را کامل کرده و اووسیت ثانویه + جسم قطبی اول می‌سازد. تخمک به آمپولار لوله رحم می‌رسد و ۳۰ ساعت توقف می‌کند. میوز II <strong>پس از لقاح</strong> کامل می‌شود. <strong>زمان باروری تخمک:</strong> ۱۲-۲۴ ساعت.</p>
<p><strong>اسپرم:</strong> اسپرماتوژنز (۷۴ روز) در بیضه انجام می‌شود: اسپرماتوگونی → اسپرماتوسیت اولیه (۲۳ جفت) → میوز I → اسپرماتوسیت ثانویه → میوز II → ۴ اسپرم (۲۳ کروموزوم). در اپیدیدیم (۱۸-۲۴ ساعت) تحرک می‌گیرند. pH واژن ۴.۵ و منی ۷.۵ است. فقط ۲۰۰ اسپرم به تخمک می‌رسند. <strong>زمان باروری اسپرم:</strong> ۴۸-۷۲ ساعت.</p>

<h2>۲. لقاح و لانه‌گزینی</h2>
<p><strong>لقاح:</strong> در آمپولار لوله رحم انجام می‌شود. مراحل: ظرفیت‌سازی → واکنش آکروزومی (آزادسازی آنزیم) → نفوذ اسپرم. واکنش زونا مانع ورود اسپرم‌های دیگر می‌شود. زیگوت با ۲۳ جفت کروموزوم تشکیل می‌شود. <strong>بیشترین احتمال باروری:</strong> ۳ روز قبل و ۱ روز بعد از تخمک‌گذاری.</p>
<p><strong>تقسیمات:</strong> تسهیم (هر ۱۲ ساعت). روز ۳-۴: مورولا (۱۲-۱۶ سلول). روز ۴-۵: بلاستوسیست (تروفوبلاست + توده سلولی داخلی). <strong>لانه‌گزینی:</strong> روز ۵-۷ پس از لقاح (معادل روز ۲۱-۲۹ سیکل) در دیواره خلفی فوندوس رحم. تا روز ۱۱-۱۲ کامل می‌شود.</p>

<h2>۳. گاسترولاسیون و دوره‌ها</h2>
<p><strong>سه لایه:</strong> اکتودرم (پوست، مو، اعصاب، آدرنال)، مزودرم (استخوان، عضله، قلب، کلیه، ژنیتال)، آندودرم (گوارش، تنفس، کبد، پانکراس). <strong>دوره‌ها:</strong> پیش‌رویانی (تا هفته ۳)، رویانی (هفته ۴-۸؛ <span style="color: #f1c40f; font-weight: bold;">⚠️ حساس‌ترین دوره به تراتوژن‌ها و اندام‌زایی</span>)، جنینی (هفته ۹ تا تولد). تراتوژن در پیش‌رویانی باعث سقط خودبه‌خودی می‌شود.</p>

<h2>۴. جدول تکامل کلیدی</h2>
<p><strong>هفته ۴:</strong> قلب شروع به ضربان می‌کند، جوانه ریه. <strong>هفته ۵:</strong> جوانه دست و پا. <strong>هفته ۶:</strong> انگشتان شکل می‌گیرد، استخوانی‌شدن آغاز می‌شود. <strong>هفته ۸-۱۰:</strong> کلیه ادرار ترشح می‌کند، جنسیت قابل تشخیص. <strong>هفته ۳۶:</strong> L/S > 2 (بلوغ ریه)، رفلکس مکیدن ضعیف، بیضه‌ها در حال نزول. <strong>هفته ۴۰:</strong> L/S > 2، پوست نرم، حرکات فعال و قابل تحمل، نزول کامل بیضه‌ها.</p>
"""

# =========================================================
# ۲. سوالات کوئیز (۲۰ سوال سطح متوسط و سخت)
# =========================================================
quiz_questions = [
    {
        "q": "لقاح معمولاً در کدام قسمت لوله رحم انجام می‌شود؟",
        "options": ["ایستموس", "آمپولار (یک‌سوم خارجی)", "اینترستیال", "اینفاندیبولار"],
        "correct": 1,
        "reason": "لقاح در قسمت آمپولار (یک‌سوم خارجی) لوله رحم انجام می‌شود که محل تلاقی اسپرم و تخمک است."
    },
    {
        "q": "اسپرماتوژنز (از اسپرماتوگونی تا اسپرم بالغ) چند روز طول می‌کشد؟",
        "options": ["۳۰ روز", "۵۰ روز", "۷۴ روز", "۹۰ روز"],
        "correct": 2,
        "reason": "طول اسپرماتوژنز حدود ۷۴ روز است. اسپرم‌ها سپس در اپیدیدیم بالغ می‌شوند."
    },
    {
        "q": "کدام هورمون باعث تکمیل میوز I در تخمک (قبل از تخمک‌گذاری) می‌شود؟",
        "options": ["FSH", "LH", "استروژن", "پروژسترون"],
        "correct": 1,
        "reason": "افزایش ناگهانی LH (سورژ LH) باعث می‌شود اووسیت اولیه میوز I را کامل کرده و اووسیت ثانویه بسازد."
    },
    {
        "q": "زمان باروری تخمک و اسپرم به ترتیب چند ساعت است؟",
        "options": ["۱۲-۲۴ و ۴۸-۷۲", "۴۸-۷۲ و ۱۲-۲۴", "۲۴-۴۸ و ۷۲-۹۶", "۶-۱۲ و ۲۴-۴۸"],
        "correct": 0,
        "reason": "تخمک ۱۲-۲۴ ساعت و اسپرم ۴۸-۷۲ ساعت قابلیت باروری دارند."
    },
    {
        "q": "مورولا (توده ۱۲-۱۶ سلولی) در چه روزی پس از لقاح تشکیل می‌شود؟",
        "options": ["روز ۱-۲", "روز ۳-۴", "روز ۵-۶", "روز ۷-۸"],
        "correct": 1,
        "reason": "مورولا در روز ۳-۴ پس از لقاح تشکیل می‌شود و سپس وارد رحم می‌شود."
    },
    {
        "q": "کدام یک از موارد زیر از مشتقات اکتودرم است؟",
        "options": ["کبد", "قلب", "سیستم عصبی", "کلیه"],
        "correct": 2,
        "reason": "اکتودرم منشأ سیستم عصبی، پوست، مو و بخش مرکزی غده آدرنال است."
    },
    {
        "q": "حساس‌ترین دوره تکامل به مواد تراتوژن کدام است؟",
        "options": ["پیش‌رویانی", "رویانی (امبریونیک)", "جنینی", "دوره بلوغ"],
        "correct": 1,
        "reason": "دوره رویانی (هفته ۴ تا ۸ پس از لقاح) دوره اندام‌زایی است و بیشترین حساسیت را به تراتوژن‌ها دارد."
    },
    {
        "q": "عارضه عوامل تراتوژن در دوره پیش‌رویانی چیست؟",
        "options": ["ناهنجاری اندام‌ها", "سقط خودبه‌خودی", "تاخیر رشد", "ناهنجاری قلبی"],
        "correct": 1,
        "reason": "در دوره پیش‌رویانی، عوامل تراتوژن معمولاً باعث سقط خودبه‌خودی می‌شوند، نه ناهنجاری."
    },
    {
        "q": "چه مکانیسمی مانع ورود اسپرم‌های دیگر به تخمک پس از لقاح می‌شود؟",
        "options": ["واکنش آکروزومی", "واکنش زونا", "ظرفیت‌سازی", "تسهیم"],
        "correct": 1,
        "reason": "پس از ورود اسپرم، واکنش زونا (Zona reaction) در لایه زونا پالسیودا رخ داده و مانع ورود اسپرم‌های دیگر می‌شود."
    },
    {
        "q": "لانه‌گزینی (Implantation) در چه روزهایی پس از لقاح کامل می‌شود؟",
        "options": ["روز ۳-۴", "روز ۵-۷", "روز ۱۱-۱۲", "روز ۱۴-۱۵"],
        "correct": 2,
        "reason": "لانه‌گزینی از روز ۵-۷ شروع شده و تا روز ۱۱-۱۲ پس از لقاح کامل می‌شود."
    },
    {
        "q": "در هفته ۳۶ بارداری، نسبت L/S (لسیتین/اسفنگومیلین) برای بلوغ ریه چقدر باید باشد؟",
        "options": ["L/S > 1", "L/S > 2", "L/S = 1", "L/S < 1"],
        "correct": 1,
        "reason": "نسبت L/S > 2 در هفته ۳۶ نشان‌دهنده بلوغ کافی ریه‌های جنین است."
    },
    {
        "q": "کدام یک از موارد زیر از مشتقات مزودرم است؟",
        "options": ["پانکراس", "بیضه‌ها و تخمدان‌ها", "دستگاه گوارش", "هیپوفیز قدامی"],
        "correct": 1,
        "reason": "مزودرم منشأ استخوان، عضله، قلب، کلیه و بیشتر قسمت‌های دستگاه ژنیتال (بیضه و تخمدان) است."
    },
    {
        "q": "زیگوت (سلول تخم) چند جفت کروموزوم دارد؟",
        "options": ["۲۳ جفت", "۴۶ جفت", "۲۲ جفت", "۲۴ جفت"],
        "correct": 0,
        "reason": "زیگوت حاصل یکی شدن هسته اسپرم (۲۳ کروموزوم) و تخمک (۲۳ کروموزوم) است و ۲۳ جفت کروموزوم دارد."
    },
    {
        "q": "در کدام هفته بارداری، جنسیت جنین از نظر داخلی و خارجی قابل تشخیص است؟",
        "options": ["هفته ۴", "هفته ۶", "هفته ۸-۱۰", "هفته ۱۲"],
        "correct": 2,
        "reason": "در هفته ۸-۱۰، اندام‌های جنسی داخلی و خارجی متمایز شده و جنسیت قابل تشخیص است."
    },
    {
        "q": "بیشترین احتمال باروری در چه بازه‌ای از زمان است؟",
        "options": ["روز تخمک‌گذاری", "۳ روز قبل و ۱ روز بعد از تخمک‌گذاری", "۱ روز قبل و ۳ روز بعد", "هفته قبل از تخمک‌گذاری"],
        "correct": 1,
        "reason": "با توجه به عمر ۱۲-۲۴ ساعته تخمک و ۴۸-۷۲ ساعته اسپرم، بیشترین احتمال باروری ۳ روز قبل و ۱ روز بعد از تخمک‌گذاری است."
    },
    {
        "q": "در هفته ۴۰ بارداری، کدام وضعیت در مورد حرکات جنین صحیح است؟",
        "options": ["حرکات ضعیف و غیرقابل تحمل", "حرکات فعال و قابل تحمل", "حرکات فقط در شب", "جنین حرکتی ندارد"],
        "correct": 1,
        "reason": "در هفته ۴۰، جنین حرکات فعال و قابل تحمل دارد، تون خوب است و می‌تواند سر را بالا ببرد."
    },
    {
        "q": "کدام یک از موارد زیر در مورد توده سلولی داخلی (Inner cell mass) صحیح است؟",
        "options": ["جفت را می‌سازد", "جنین و پرده آمنیون را می‌سازد", "حفره بلاستوسل را می‌سازد", "تروفوبلاست را می‌سازد"],
        "correct": 1,
        "reason": "توده سلولی داخلی (قطب جنینی) بعدها جنین و پرده آمنیون را می‌سازد. تروفوبلاست جفت را می‌سازد."
    },
    {
        "q": "کدام لایه جنینی منشأ دستگاه تنفس و گوارش است؟",
        "options": ["اکتودرم", "مزودرم", "آندودرم", "اپی‌بلاست"],
        "correct": 2,
        "reason": "آندودرم (داخلی‌ترین لایه) منشأ دستگاه گوارش، تنفس، کبد، پانکراس و سیستم صفراوی است."
    },
    {
        "q": "پس از انزال، عوامل مهاری اسپرم چه زمانی از بین می‌روند؟",
        "options": ["در اپیدیدیم", "در بیضه", "پس از تماس با مجاری زن", "هرگز از بین نمی‌روند"],
        "correct": 2,
        "reason": "عوامل مهاری موجود در مجاری مردانه، پس از انزال و تماس با مجاری تناسلی زن (ظرفیت‌سازی) از بین می‌روند."
    },
    {
        "q": "کدام هورمون در زمان تخمک‌گذاری با افزایش ترشحات گردن رحم به انتقال اسپرم کمک می‌کند؟",
        "options": ["پروژسترون", "استروژن", "LH", "FSH"],
        "correct": 1,
        "reason": "بالا بودن سطح استروژن در زمان تخمک‌گذاری باعث افزایش ترشحات گردن رحم و کاهش ویسکوزیته آن‌ها می‌شود که به انتقال اسپرم کمک می‌کند."
    }
]

# =========================================================
# ۳. توابع کمکی
# =========================================================
def load_bookmarks():
    if os.path.exists("bookmarks.json"):
        with open("bookmarks.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_bookmarks(bookmarks):
    with open("bookmarks.json", "w", encoding="utf-8") as f:
        json.dump(bookmarks, f, ensure_ascii=False, indent=4)

# =========================================================
# ۴. HTML و CSS (طرح شیک، مدرن، تیره)
# =========================================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Embryo Pro | ابزار هوشمند جنین‌شناسی</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        /* ===== تنظیمات پایه و تم تاریک (مثل عکس) ===== */
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', 'Tahoma', sans-serif;
            background: #0b0b1a; /* رنگ پس‌زمینه تیره */
            color: #e0e0e0;
            padding: 20px;
            background-image: radial-gradient(circle at 10% 20%, rgba(40, 20, 80, 0.4) 0%, transparent 40%);
            min-height: 100vh;
        }
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #16162e; }
        ::-webkit-scrollbar-thumb { background: #7c3aed; border-radius: 10px; }

        /* ===== کانتینر اصلی و افکت شیشه‌ای ===== */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 25px;
        }
        .glass-panel {
            background: rgba(30, 30, 70, 0.6);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 24px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
            transition: all 0.3s ease;
        }
        .glass-panel:hover { border-color: rgba(124, 58, 237, 0.3); }

        /* ===== هدر و نوار ابزار ===== */
        .header { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; }
        .logo h1 { font-size: 1.8em; color: #fff; background: linear-gradient(135deg, #7c3aed, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .logo span { font-size: 0.5em; -webkit-text-fill-color: #888; }
        
        .toolbar { display: flex; gap: 10px; flex-wrap: wrap; }
        .toolbar button, .toolbar input {
            padding: 10px 20px;
            border: none;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.05);
            color: #fff;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        .toolbar button:hover { background: #7c3aed; transform: translateY(-2px); box-shadow: 0 5px 15px rgba(124, 58, 237, 0.4); }
        .toolbar input { flex: 1; min-width: 150px; background: rgba(0,0,0,0.3); outline: none; }
        .toolbar input:focus { border-color: #7c3aed; }

        /* ===== خلاصه مطالب ===== */
        .summary-content h2 { color: #a78bfa; margin: 25px 0 10px 0; font-size: 1.5em; }
        .summary-content h2:first-child { margin-top: 0; }
        .summary-content p { color: #cbd5e1; line-height: 1.9; margin-bottom: 15px; text-align: justify; }
        .summary-content strong { color: #f8fafc; }

        /* ===== کوئیز (باکس مدرن) ===== */
        .quiz-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .score-badge { background: #1e1e4a; padding: 8px 15px; border-radius: 20px; border: 1px solid #7c3aed; }
        .options-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 20px 0; }
        .option-btn {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 12px;
            color: #cbd5e1;
            cursor: pointer;
            text-align: right;
            transition: 0.3s;
            font-size: 1em;
        }
        .option-btn:hover { background: rgba(124, 58, 237, 0.2); border-color: #7c3aed; }
        .option-btn.correct { background: rgba(16, 185, 129, 0.3); border-color: #10b981; color: #10b981; }
        .option-btn.wrong { background: rgba(239, 68, 68, 0.3); border-color: #ef4444; color: #ef4444; }
        .option-btn.disabled { cursor: not-allowed; opacity: 0.7; }
        
        .quiz-reason { background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 12px; border-right: 4px solid #7c3aed; margin: 15px 0; display: none; }
        .quiz-nav { display: flex; justify-content: space-between; gap: 15px; margin-top: 20px; }
        .quiz-nav button { background: #7c3aed; padding: 10px 30px; border: none; border-radius: 12px; color: white; font-weight: bold; cursor: pointer; transition: 0.3s; flex: 1; }
        .quiz-nav button:hover { background: #6d28d9; }
        .quiz-nav button:disabled { opacity: 0.5; cursor: not-allowed; }

        /* ===== تایم‌لاین افقی (مثل عکس) ===== */
        .timeline-wrapper { display: flex; justify-content: space-around; flex-wrap: wrap; gap: 10px; padding: 10px 0; }
        .timeline-item {
            background: rgba(255, 255, 255, 0.03);
            padding: 15px;
            border-radius: 16px;
            text-align: center;
            min-width: 100px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            flex: 1;
        }
        .timeline-item .week { font-size: 1.2em; font-weight: bold; color: #a78bfa; }
        .timeline-item .desc { font-size: 0.8em; color: #94a3b8; margin-top: 5px; }

        /* ===== واکنش‌گرا ===== */
        @media (max-width: 768px) {
            .options-grid { grid-template-columns: 1fr; }
            .header { flex-direction: column; align-items: stretch; }
            .timeline-item { min-width: 80px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- ===== هدر ===== -->
        <div class="glass-panel">
            <div class="header">
                <div class="logo">
                    <h1>Embryo Pro <span>| مطالعه هوشمند</span></h1>
                </div>
                <div class="toolbar">
                    <input type="text" id="searchInput" placeholder="جستجو در متن... (مثلاً: لقاح)">
                    <button onclick="performSearch()"><i class="fas fa-search"></i> جستجو</button>
                    <button onclick="resetHighlights()"><i class="fas fa-undo"></i> پاک‌سازی</button>
                </div>
            </div>
        </div>

        <!-- ===== تایم‌لاین ===== -->
        <div class="glass-panel">
            <h3 style="color: #a78bfa; margin-bottom: 15px;">⏳ تایم‌لاین رشد</h3>
            <div class="timeline-wrapper">
                <div class="timeline-item"><div class="week">۱-۳</div><div class="desc">پیش‌رویانی</div></div>
                <div class="timeline-item" style="border-color: #f59e0b;"><div class="week" style="color: #f59e0b;">۴-۸</div><div class="desc">⚠️ رویانی (اندام‌زایی)</div></div>
                <div class="timeline-item"><div class="week">۹-۴۰</div><div class="desc">جنینی</div></div>
                <div class="timeline-item"><div class="week">۳۶</div><div class="desc">L/S > 2</div></div>
                <div class="timeline-item"><div class="week">۴۰</div><div class="desc">تولد</div></div>
            </div>
        </div>

        <!-- ===== خلاصه مطالب ===== -->
        <div class="glass-panel">
            <h3 style="color: #a78bfa; margin-bottom: 15px;">📖 خلاصه جامع (فشرده)</h3>
            <div class="summary-content">
                {{ summary|safe }}
            </div>
        </div>

        <!-- ===== کوئیز تستی ===== -->
        <div class="glass-panel" id="quizPanel">
            <div class="quiz-header">
                <h3 style="color: #a78bfa;">🎯 کوئیز پیشرفته (۲۰ سوال)</h3>
                <div class="score-badge">
                    درست: <span id="correctCount">0</span> | غلط: <span id="wrongCount">0</span>
                </div>
            </div>
            <div id="quizContainer">
                <h4 id="qTitle" style="color: #f8fafc; margin-bottom: 10px;">برای شروع، دکمه "شروع کوئیز" را بزنید.</h4>
                <div id="optionsContainer" class="options-grid"></div>
                <div id="reasonBox" class="quiz-reason"></div>
                <div class="quiz-nav">
                    <button id="prevBtn" onclick="prevQuestion()" disabled>قبلی</button>
                    <button id="nextBtn" onclick="nextQuestion()">بعدی</button>
                </div>
                <div style="text-align: center; margin-top: 15px;">
                    <button onclick="startQuiz()" style="background: transparent; border: 1px solid #7c3aed; color: #fff; padding: 10px 30px; border-radius: 12px; cursor: pointer;">🔄 شروع مجدد کوئیز</button>
                </div>
            </div>
        </div>
    </div>

    <!-- ================================ -->
    <!-- ===== جاوااسکریپت داخل فایل ===== -->
    <!-- ================================ -->
    <script>
        let quizData = [];
        let currentQuestionIndex = 0;
        let correctAnswers = 0;
        let wrongAnswers = 0;
        let isAnswered = false;

        // ===== جستجو و هایلایت =====
        function performSearch() {
            const query = document.getElementById('searchInput').value.trim();
            if (!query) return alert('لطفاً کلمه‌ای وارد کنید.');
            resetHighlights();
            const contentDiv = document.querySelector('.summary-content');
            const text = contentDiv.innerHTML;
            if (text.includes(query)) {
                contentDiv.innerHTML = text.replace(new RegExp(query, 'g'), `<span style="background: #7c3aed; color: #fff; padding: 2px 5px; border-radius: 4px;">${query}</span>`);
            } else {
                alert('نتیجه‌ای یافت نشد!');
            }
        }

        function resetHighlights() {
            const contentDiv = document.querySelector('.summary-content');
            const spans = contentDiv.querySelectorAll('span[style*="background: #7c3aed"]');
            spans.forEach(span => {
                span.outerHTML = span.innerText;
            });
        }

        // ===== کوئیز =====
        function startQuiz() {
            // شافل کردن سوالات
            quizData = {{ quiz_questions|tojson }};
            quizData = quizData.sort(() => Math.random() - 0.5);
            currentQuestionIndex = 0;
            correctAnswers = 0;
            wrongAnswers = 0;
            isAnswered = false;
            document.getElementById('correctCount').innerText = '0';
            document.getElementById('wrongCount').innerText = '0';
            renderQuestion();
        }

        function renderQuestion() {
            if (quizData.length === 0) return;
            const q = quizData[currentQuestionIndex];
            document.getElementById('qTitle').innerHTML = `<strong>سوال ${currentQuestionIndex + 1} از ${quizData.length}:</strong> ${q.q}`;
            
            const optionsContainer = document.getElementById('optionsContainer');
            optionsContainer.innerHTML = '';
            isAnswered = false;

            // دکمه‌های قبلی/بعدی
            document.getElementById('prevBtn').disabled = (currentQuestionIndex === 0);
            document.getElementById('nextBtn').disabled = false;

            // ایجاد گزینه‌ها
            q.options.forEach((opt, index) => {
                const btn = document.createElement('button');
                btn.className = 'option-btn';
                btn.innerText = `${String.fromCharCode(65 + index)}. ${opt}`; // A, B, C, D
                btn.onclick = () => checkAnswer(index, btn);
                optionsContainer.appendChild(btn);
            });

            document.getElementById('reasonBox').style.display = 'none';
            document.getElementById('reasonBox').innerHTML = '';
        }

        function checkAnswer(selectedIndex, btnElement) {
            if (isAnswered) return;
            isAnswered = true;
            const q = quizData[currentQuestionIndex];
            const allBtns = document.querySelectorAll('.option-btn');
            
            // غیرفعال کردن همه دکمه‌ها
            allBtns.forEach(b => b.classList.add('disabled'));

            // نمایش جواب درست و غلط
            allBtns.forEach((b, idx) => {
                if (idx === q.correct) b.classList.add('correct');
                if (idx === selectedIndex && idx !== q.correct) b.classList.add('wrong');
            });

            // نمایش دلیل
            const reasonBox = document.getElementById('reasonBox');
            if (selectedIndex === q.correct) {
                correctAnswers++;
                document.getElementById('correctCount').innerText = correctAnswers;
                reasonBox.innerHTML = `<span style="color: #10b981;">✅ درست!</span> ${q.reason}`;
            } else {
                wrongAnswers++;
                document.getElementById('wrongCount').innerText = wrongAnswers;
                reasonBox.innerHTML = `<span style="color: #ef4444;">❌ غلط!</span> پاسخ صحیح گزینه ${String.fromCharCode(65 + q.correct)} است. ${q.reason}`;
            }
            reasonBox.style.display = 'block';
        }

        function nextQuestion() {
            if (currentQuestionIndex < quizData.length - 1) {
                currentQuestionIndex++;
                renderQuestion();
            } else {
                alert('🎉 تمام سوالات پاسخ داده شد! برای امتحان مجدد دکمه "شروع مجدد" را بزنید.');
                document.getElementById('nextBtn').disabled = true;
            }
        }

        function prevQuestion() {
            if (currentQuestionIndex > 0) {
                currentQuestionIndex--;
                renderQuestion();
            }
        }

        // اجرای خودکار در شروع
        startQuiz();
    </script>
</body>
</html>
"""

# =========================================================
# ۵. مسیرهای Flask
# =========================================================
@app.route('/')
def index():
    return render_template_string(
        HTML_TEMPLATE,
        summary=summary_content,
        quiz_questions=quiz_questions
    )

if __name__ == '__main__':
    print("🚀 Embryo Pro راه‌اندازی شد!")
    print("🌐 آدرس: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)