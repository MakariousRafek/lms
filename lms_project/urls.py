from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 1. لوحة تحكم الإدارة (Django Admin)
    path('admin/', admin.site.urls),

    # 2. ربط المشروع كله بتطبيق المسابقات (course)
    # السطر ده هيخلي ديجانجو يروح يدور في course/urls.py
    # وهناك هيلاقي دالة اللوجن الذكية بتاعتك وكل الدوال التانية
    path('', include('course.urls')),
]