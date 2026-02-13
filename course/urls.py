from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 1. صفحة اللوجن (لازم تشاور على الدالة الذكية بتاعتك)
    path('login/', views.custom_login_view, name='login'), # السطر ده هو مفتاح الحل

    # 2. عسكري المرور: أول صفحة بتفتح بعد اللوجن
    path('', views.home_redirect, name='home_redirect'),
    path('home-redirect/', views.home_redirect, name='home_redirect'),

    # 3. روابط الطالبة (Student)
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('lesson/<int:lesson_id>/quiz/', views.lesson_quiz, name='lesson_quiz'),

    # 4. روابط لوحة تحكم تاسوني (Admin Dashboard)
    path('dashboard/', views.custom_admin_dashboard, name='dashboard'),
    path('dashboard/add-lesson/', views.add_lesson, name='add_lesson'),
    path('dashboard/add-user/', views.add_custom_user, name='add_custom_user'),
    path('dashboard/delete-user/<int:user_id>/', views.delete_user, name='delete_user'),

    # 5. رابط تصحيح المقالي
    path('grade-essays/<int:progress_id>/', views.grade_essays, name='grade_essays'),

    # 6. تسجيل الخروج
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
path('dashboard/edit-lesson/<int:lesson_id>/', views.edit_lesson, name='edit_lesson'),

]