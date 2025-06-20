# خطوات النشر على Render.com

## 1. تحضير الملفات

تأكد من وجود الملفات التالية في مجلد المشروع:
- ✅ `app.py`
- ✅ `requirements.txt`
- ✅ `Procfile`
- ✅ `config.py`
- ✅ `init_db.py`
- ✅ مجلد `templates/`
- ✅ مجلد `static/`

## 2. رفع المشروع إلى GitHub

```bash
git init
git add .
git commit -m "Initial commit - Rivaq Task Management System"
git branch -M main
git remote add origin https://github.com/yourusername/rivaq-flask-system.git
git push -u origin main
```

## 3. إنشاء خدمة على Render

1. اذهب إلى [render.com](https://render.com)
2. سجل دخول أو أنشئ حساب جديد
3. اضغط على "New +" ثم "Web Service"
4. اربط حساب GitHub الخاص بك
5. اختر المستودع `rivaq-flask-system`

## 4. إعدادات الخدمة

### الإعدادات الأساسية:
- **Name**: `rivaq-task-management`
- **Environment**: `Python 3`
- **Region**: اختر الأقرب لك
- **Branch**: `main`

### أوامر البناء والتشغيل:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

## 5. متغيرات البيئة

في تبويب "Environment"، أضف:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | `rivaq-secret-key-2024-very-secure-production` |
| `FLASK_ENV` | `production` |
| `DATABASE_URL` | `sqlite:///rivaq.db` |

## 6. النشر

1. اضغط "Create Web Service"
2. انتظر حتى يكتمل البناء (5-10 دقائق)
3. ستحصل على رابط مثل: `https://rivaq-task-management.onrender.com`

## 7. إعداد قاعدة البيانات

بعد النشر الأول، قم بتشغيل:
```bash
# في وحدة التحكم (Console) في Render
python init_db.py
```

## 8. اختبار النظام

1. اذهب إلى الرابط المُنشأ
2. جرب تسجيل الدخول بالحسابات التجريبية:
   - `majed@rwaqeng.com` / `Maj@100200300`
   - `asala.alsaaf@rwaqeng.com` / `100200300@Aasala`

## 9. إعدادات إضافية (اختيارية)

### تفعيل HTTPS:
- Render يوفر HTTPS تلقائياً

### نطاق مخصص:
- في إعدادات الخدمة، أضف النطاق المخصص

### مراقبة الأداء:
- استخدم تبويب "Metrics" لمراقبة الأداء

## 10. استكشاف الأخطاء

### إذا فشل البناء:
1. تحقق من ملف `requirements.txt`
2. تأكد من وجود `Procfile`
3. راجع سجلات البناء في "Logs"

### إذا لم يعمل النظام:
1. تحقق من متغيرات البيئة
2. راجع سجلات التشغيل
3. تأكد من تشغيل `init_db.py`

## 11. التحديثات المستقبلية

لتحديث النظام:
```bash
git add .
git commit -m "Update description"
git push origin main
```

سيتم إعادة النشر تلقائياً.

## ملاحظات مهمة:

- ⚠️ **قاعدة البيانات**: ستُحذف عند إعادة النشر (استخدم PostgreSQL للإنتاج)
- 🔒 **الأمان**: غيّر `SECRET_KEY` لقيمة فريدة وآمنة
- 📧 **البريد الإلكتروني**: اختياري، لتفعيل الإشعارات
- 💾 **النسخ الاحتياطي**: احفظ نسخة من قاعدة البيانات دورياً

## الدعم:

للمساعدة أو الاستفسارات، راجع:
- [وثائق Render](https://render.com/docs)
- [وثائق Flask](https://flask.palletsprojects.com/)
- ملف `README.md` في المشروع

