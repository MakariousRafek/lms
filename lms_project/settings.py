import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-^q808xp^1o#eau2z1413uqr2kjt8cwb)sw3e+adxc2echf^7#r'

# خليه False عند الرفع الفعلي للأمان
DEBUG = True 

# السماح برابط Render الجديد
ALLOWED_HOSTS = ['*', '.onrender.com'] 

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'course', 
    'whitenoise.runserver_nostatic', # إضافة مكتبة الصور
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # ضروري جداً لظهور الصور على Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ... (باقي الإعدادات زي ما هي عندك)

# إعدادات ملفات الـ Static (الصور والـ CSS)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# إضافة روابط Render الموثوقة لـ CSRF
CSRF_TRUSTED_ORIGINS = [
    'https://makarious.pythonanywhere.com',
    'https://*.onrender.com' # أي رابط هيطلعهولك Render هيكون شغال
]

# إعدادات اللوجن (تأكد إن المسارات مطابقة للـ urls.py عندك)
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home_redirect'
LOGOUT_REDIRECT_URL = 'login'
