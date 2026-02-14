import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _ # ضروري لترجمة أسماء اللغات

# 1. المسارات الأساسية
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. الأمان
SECRET_KEY = 'django-insecure-^q808xp^1o#eau2z1413uqr2kjt8cwb)sw3e+adxc2echf^7#r'
DEBUG = True
ALLOWED_HOSTS = ['*', '.onrender.com']

# 3. التطبيقات المضافة
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'course',
    'whitenoise.runserver_nostatic',
]

# 4. الـ Middleware (الترتيب هنا هو سر الحل)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # 1. السشن أولاً
    'django.middleware.locale.LocaleMiddleware',           # 2. اللغة ثانياً (مكانها هنا بالظبط)
    'django.middleware.common.CommonMiddleware',           # 3. الكومون ثالثاً
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lms_project.urls'

# 5. القوالب (إضافة context_processor اللغة)
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
                'django.template.context_processors.i18n', # ضروري عشان القالب يحس باللغة
            ],
        },
    },
]

WSGI_APPLICATION = 'lms_project.wsgi.application'

# 6. الداتابيز
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 7. إعدادات اللغات الدولية
LANGUAGE_CODE = 'ar' # اللغة الافتراضية

LANGUAGES = [
    ('ar', _('Arabic')),
    ('en', _('English')),
]

USE_I18N = True # تفعيل الترجمة
USE_L10N = True
USE_TZ = True

# إجبار المتصفح على حفظ اللغة في الكوكيز
LANGUAGE_COOKIE_NAME = 'django_language'
LANGUAGE_COOKIE_AGE = 31536000 # سنة كاملة
LANGUAGE_COOKIE_PATH = '/'

# 8. الـ Static Files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 9. إعدادات الحماية واللوجن
CSRF_TRUSTED_ORIGINS = [
    'https://makarious.pythonanywhere.com',
    'https://*.onrender.com'
]

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home_redirect'
LOGOUT_REDIRECT_URL = 'login'