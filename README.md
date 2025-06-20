# نظام إدارة المهام - شركة رِواق للاستشارات الهندسية

نظام شامل لإدارة المهام والاجتماعات والمستخدمين مبني بتقنية Flask.

## المتطلبات

- Python 3.8+
- Flask 3.0+
- SQLite (مدمج مع Python)

## التثبيت والتشغيل

### 1. تثبيت المتطلبات

```bash
pip install -r requirements.txt
```

### 2. إعداد قاعدة البيانات

```bash
python init_db.py
```

### 3. تشغيل التطبيق

```bash
python app.py
```

أو للإنتاج:

```bash
gunicorn app:app
```

## الميزات

### إدارة المستخدمين
- 20 مستخدم حقيقي من بيانات الشركة
- نظام صلاحيات متقدم
- إدارة المدراء المباشرين
- تواريخ الانضمام

### إدارة المهام
- إنشاء وتعديل وحذف المهام
- إسناد المهام للموظفين
- نظام الأولويات والحالات
- تتبع التقدم بالنسبة المئوية
- البحث والتصفية المتقدم

### إدارة الاجتماعات (نموذج GROW)
- **Goal (الهدف)**: تحديد أهداف الاجتماع
- **Reality (الواقع)**: تحليل الوضع الحالي
- **Options (الخيارات)**: استكشاف البدائل
- **Way Forward (الطريق للأمام)**: تحديد الخطوات التالية
- إضافة المستخدمين للاجتماعات
- نظام فهرسة ومتابعة

### التقارير والإحصائيات
- تقارير الأداء
- إحصائيات المهام
- تقارير الاجتماعات
- تحليلات تفصيلية
- إمكانية التصدير

## بيانات الدخول التجريبية

| البريد الإلكتروني | كلمة المرور | المنصب |
|-------------------|-------------|---------|
| majed@rwaqeng.com | Maj@100200300 | الرئيس التنفيذي |
| asala.alsaaf@rwaqeng.com | 100200300@Aasala | مدير تطوير الأعمال |
| muhanad.bk@rwaqeng.com | Muh@100200300 | نائب الرئيس |
| nawar.sammani@rwaqeng.com | Naw@100200300 | مدير القسم الفني |

## هيكل المشروع

```
rivaq-flask-system/
├── app.py                 # التطبيق الرئيسي
├── config.py             # إعدادات النظام
├── init_db.py            # إعداد قاعدة البيانات
├── requirements.txt      # المتطلبات
├── Procfile             # إعدادات النشر
├── templates/           # قوالب HTML
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── tasks.html
│   ├── users.html
│   ├── meetings.html
│   ├── reports.html
│   └── profile.html
├── static/              # الملفات الثابتة
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── images/
│       └── rivaq-logo.png
└── rivaq.db            # قاعدة البيانات (تُنشأ تلقائياً)
```

## قاعدة البيانات

النظام يستخدم SQLite مع الجداول التالية:

- **users**: بيانات المستخدمين والصلاحيات
- **tasks**: المهام والمشاريع
- **meetings**: الاجتماعات ونموذج GROW
- **meeting_outputs**: مخرجات الاجتماعات

## النشر

### Render.com

1. ارفع الملفات إلى GitHub
2. اربط المستودع مع Render
3. اختر "Web Service"
4. استخدم الإعدادات:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

### Heroku

```bash
git init
git add .
git commit -m "Initial commit"
heroku create your-app-name
git push heroku main
```

## متغيرات البيئة

```bash
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///rivaq.db
FLASK_ENV=production
```

## الدعم والصيانة

للدعم التقني أو الاستفسارات، يرجى التواصل مع فريق التطوير.

## الترخيص

هذا النظام مطور خصيصاً لشركة رِواق للاستشارات الهندسية.
جميع الحقوق محفوظة © 2024

