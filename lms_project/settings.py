import os
from pathlib import Path

# 1. المسارات الأساسية
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. الأمان (خلى DEBUG بـ True عشان نشوف الإيرورز لو حصلت حالياً)
SECRET_KEY = 'django-insecure-^q808xp^1o#eau2z1413uqr2kjt8cwb)sw3e+adxc2echf^7#r'
DEBUG = True
ALLOWED_HOSTS = ['*', '.onrender.com'] #

# 3. التطبيقات المضافة
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'course',
    'whitenoise.runserver_nostatic', # لضمان تشغيل الصور
]

# 4. الـ Middleware (ترتيب Whitenoise مهم جداً)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # لازم يكون السطر التاني
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lms_project.urls'

# 5. حل إيرور admin.E403 (تأكد من وجود هذا الجزء بالكامل)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'lms_project.wsgi.application'

# 6. الداتابيز (تستخدم SQLite حالياً لسهولة الرفع المجاني)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 7. الـ Static Files (عشان اللوجو يظهر على Render)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 8. إعدادات الحماية واللوجن
CSRF_TRUSTED_ORIGINS = [
    'https://makarious.pythonanywhere.com',
    'https://*.onrender.com'
]

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home_redirect'
LOGOUT_REDIRECT_URL = 'login'