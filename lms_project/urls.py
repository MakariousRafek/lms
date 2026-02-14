from django.contrib import admin
from django.urls import path, include  # ضروري تضيف include هنا
from django.views.generic import RedirectView # استيراد للتحويل التلقائي
from course.views import (
    custom_login_view,
    signup_view,
    home_redirect,
    custom_admin_dashboard,
    student_dashboard,
    lesson_detail,
    lesson_quiz,
    grade_essays,
    add_lesson,
    edit_lesson,
    add_custom_user,
    delete_user
)
from django.contrib.auth.views import LogoutView # استيراد دالة الخروج الافتراضية

urlpatterns = [
path('', RedirectView.as_view(url='login/'), name='go-to-login'),
    path('admin/', admin.site.urls),

    # السطر ده هو اللي هيخلي اللغة تتغير فعلياً
    path('i18n/', include('django.conf.urls.i18n')),

    # روابط الدخول والتسجيل
    path('login/', custom_login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('home-redirect/', home_redirect, name='home_redirect'),

    # لوحة التحكم
    path('dashboard/', custom_admin_dashboard, name='dashboard'),
    path('student/', student_dashboard, name='student_dashboard'),

    # روابط الدروس والاختبارات
    path('lesson/<int:lesson_id>/', lesson_detail, name='lesson_detail'),
    path('lesson/<int:lesson_id>/quiz/', lesson_quiz, name='lesson_quiz'),

    # إدارة المحتوى
    path('dashboard/add-lesson/', add_lesson, name='add_lesson'),
    path('dashboard/edit-lesson/<int:lesson_id>/', edit_lesson, name='edit_lesson'),
    path('dashboard/add-user/', add_custom_user, name='add_custom_user'),
    path('dashboard/delete-user/<int:user_id>/', delete_user, name='delete_user'),
    path('grade-essays/<int:progress_id>/', grade_essays, name='grade_essays'),
path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]