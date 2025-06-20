# متغيرات البيئة المطلوبة للنشر على Render

## المتغيرات الأساسية:

### 1. SECRET_KEY
```
SECRET_KEY=rivaq-secret-key-2024-very-secure-production-key
```

### 2. FLASK_ENV
```
FLASK_ENV=production
```

### 3. DATABASE_URL (اختياري - سيستخدم SQLite افتراضياً)
```
DATABASE_URL=sqlite:///rivaq.db
```

## المتغيرات الاختيارية:

### 4. إعدادات البريد الإلكتروني (للإشعارات)
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### 5. إعدادات رفع الملفات
```
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=static/uploads
```

## خطوات إعداد متغيرات البيئة في Render:

1. اذهب إلى لوحة تحكم Render
2. اختر الخدمة (Web Service)
3. اذهب إلى تبويب "Environment"
4. أضف المتغيرات التالية:

| Key | Value |
|-----|-------|
| SECRET_KEY | rivaq-secret-key-2024-very-secure-production-key |
| FLASK_ENV | production |
| DATABASE_URL | sqlite:///rivaq.db |

## ملاحظات مهمة:

- **SECRET_KEY**: يجب أن يكون فريداً وآمناً
- **DATABASE_URL**: سيتم إنشاء قاعدة البيانات تلقائياً عند أول تشغيل
- **MAIL_**: اختيارية، فقط إذا كنت تريد إرسال إشعارات بالبريد الإلكتروني

## للتطوير المحلي:

انسخ ملف `.env.template` إلى `.env` وعدّل القيم حسب بيئتك المحلية.

