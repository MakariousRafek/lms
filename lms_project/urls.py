from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from django.http import HttpResponse

def create_admin_auto(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin2004')
        return HttpResponse("مبروك يا بطل! حساب الأدمن اتعمل: admin والباسورد admin2004")
    return HttpResponse("الأدمن موجود فعلاً يا هندسة!")


from django.contrib.auth.models import User
from course.models import StudentProgress, Lesson, Question, EssayAnswer


def reset_database(request):
    # مسح كل البيانات ما عدا الأدمن اللي إنت لسه عامله
    StudentProgress.objects.all().delete()
    EssayAnswer.objects.all().delete()
    Lesson.objects.all().delete()
    Question.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()

    return HttpResponse("تم تصفير الداتابيز بنجاح! الموقع الآن جاهز لاستقبال البنات.")
urlpatterns = [
    # 1. لوحة تحكم الإدارة (Django Admin)
    path('admin/', admin.site.urls),
path('make-me-admin/', create_admin_auto),
path('clear-all-data-now/', reset_database),
    # 2. ربط المشروع كله بتطبيق المسابقات (course)
    # السطر ده هيخلي ديجانجو يروح يدور في course/urls.py
    # وهناك هيلاقي دالة اللوجن الذكية بتاعتك وكل الدوال التانية
    path('', include('course.urls')),
]