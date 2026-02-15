from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.forms import inlineformset_factory
from django.db.models import Sum, F
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from .models import Lesson, Question, StudentProgress, EssayAnswer
from .forms import LessonForm, AddUserForm
from django import forms # ضروري لفورم التسجيل

# ==========================================
# 1. نظام الدخول والتسجيل الذاتي 🌸
# ==========================================

# فورم تسجيل الطالبات الجديد
class StudentSignUpForm(forms.Form):
    username = forms.CharField(max_length=150, label="اسم الطالبة الثنائي")
    password = forms.CharField(widget=forms.PasswordInput, label="كلمة المرور")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="تأكيد كلمة المرور")


from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages  # استيراد نظام الرسائل


def signup_view(request):
    error_msg = None
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            # 1. حل مشكلة التكرار لمنع الـ IntegrityError
            if User.objects.filter(username=username).exists():
                error_msg = "الاسم ده متسجل قبل كدة، جربي اسم تاني أو ادخلي لوجن 🎀"

            # 2. التأكد من تطابق كلمة المرور
            elif password != confirm_password:
                error_msg = "كلمتي المرور غير متطابقتين ❌"

            else:
                # 3. إنشاء الحساب الجديد في نيون ودخول أوتوماتيكي
                user = User.objects.create_user(username=username, password=password)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, f"أهلاً بيكي يا {username} في كوكب البرية! ✨")
                return redirect('home_redirect')
        else:
            # في حالة وجود أخطاء في الـ Form نفسه
            error_msg = "تأكدي من صحة البيانات المكتوبة 🧐"
    else:
        form = StudentSignUpForm()

    # نرسل المتغير باسم 'error' عشان يطابق الكود اللي في الـ Template بتاعك
    return render(request, 'registration/signup.html', {'form': form, 'error': error_msg})

@csrf_exempt
def custom_login_view(request):
    error_msg = None
    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')

        user = User.objects.filter(username=user_name).first()

        if user:
            # محاولة تسجيل دخول عادية
            auth_user = authenticate(request, username=user_name, password=pass_word)

            if auth_user:
                login(request, auth_user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('home_redirect')
            else:
                # نظام الدخول الذكي لأول مرة
                if not user.has_usable_password():
                    user.set_password(pass_word)
                    user.save()
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('home_redirect')
                else:
                    error_msg = "كلمة المرور غير صحيحة ❌"
        else:
            error_msg = "الاسم مش موجود، تقدري تسجلي حساب جديد من تحت 🎀"

    return render(request, 'registration/login.html', {'error': error_msg})


@login_required
def home_redirect(request):
    if request.user.is_staff:
        return redirect('dashboard')
    return redirect('student_dashboard')


# ==========================================
# 2. لوحة تحكم تاسوني (حل إيرور total_points)
# ==========================================
@staff_member_required
def custom_admin_dashboard(request):
    all_progress = StudentProgress.objects.all().select_related('user', 'lesson').order_by('-id')
    lessons = Lesson.objects.all()

    # حساب النقط بتجنب إيرور total_score
    all_students = User.objects.filter(is_staff=False).annotate(
        total_points=Sum('studentprogress__quiz_score')
    ).order_by('-total_points')

    top_students = all_students[:3]

    return render(request, 'course/admin_dashboard.html', {
        'all_progress': all_progress,
        'lessons': lessons,
        'all_students': all_students,
        'top_students': top_students
    })


# ==========================================
# 3. حل الاختبار (MCQ + حفظ المقالي)
# ==========================================
@login_required
def lesson_quiz(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = lesson.questions.all()

    if request.method == 'POST':
        progress, created = StudentProgress.objects.get_or_create(user=request.user, lesson=lesson)
        score = 0

        for q in questions:
            user_ans = request.POST.get(f'question_{q.id}')
            if q.question_type == 'mcq' and user_ans:
                if int(user_ans) == q.correct_option:
                    score += q.points
            elif q.question_type == 'text' and user_ans:
                EssayAnswer.objects.update_or_create(
                    progress=progress,
                    question=q,
                    defaults={'answer_text': user_ans}
                )

        progress.quiz_score = score
        progress.is_completed = True
        progress.save()

        return render(request, 'course/result.html', {'score': score, 'lesson': lesson})

    return render(request, 'course/lesson_quiz.html', {'lesson': lesson, 'questions': questions})


# ==========================================
# 4. تصحيح المقالي (بإضافة سطر الدرجات)
# ==========================================
@staff_member_required
def grade_essays(request, progress_id):
    progress = get_object_or_404(StudentProgress, id=progress_id)
    essays = progress.essay_answers.all()

    if request.method == 'POST':
        total_essay_grade = 0
        for essay in essays:
            grade = request.POST.get(f'grade_{essay.id}')
            if grade:
                essay.grade = int(grade)
                essay.is_graded = True
                essay.save()
                total_essay_grade += int(grade)

        progress.quiz_score += total_essay_grade
        progress.is_graded = True
        progress.save()

        return redirect('dashboard')

    return render(request, 'course/grade_essays.html', {'progress': progress, 'essays': essays})


# ==========================================
# 5. إدارة المسابقات (إضافة وتعديل)
# ==========================================
@staff_member_required
def add_lesson(request):
    QuestionFormSet = inlineformset_factory(
        Lesson, Question,
        fields=('question_type', 'question_text', 'option_1', 'option_2', 'option_3', 'option_4', 'correct_option', 'points'),
        extra=1, can_delete=True
    )
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save()
            formset = QuestionFormSet(request.POST, instance=lesson)
            if formset.is_valid():
                formset.save()
                return redirect('dashboard')
    else:
        form = LessonForm()
        formset = QuestionFormSet()
    return render(request, 'course/add_lesson.html', {'form': form, 'formset': formset})


@staff_member_required
def edit_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    QuestionFormSet = inlineformset_factory(
        Lesson, Question,
        fields=('question_type', 'question_text', 'option_1', 'option_2', 'option_3', 'option_4', 'correct_option', 'points'),
        extra=0, can_delete=True
    )
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        formset = QuestionFormSet(request.POST, instance=lesson)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('dashboard')
    else:
        form = LessonForm(instance=lesson)
        formset = QuestionFormSet(instance=lesson)
    return render(request, 'course/add_lesson.html', {'form': form, 'formset': formset, 'edit_mode': True})


# ==========================================
# 6. إدارة المستخدمين (إضافة وحذف)
# ==========================================
from django.contrib import messages  # عشان نظهر رسالة الخطأ للبنت

from django.contrib import messages


@staff_member_required
def add_custom_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            role = form.cleaned_data['role']

            # 1. التشييك على الاسم
            if User.objects.filter(username=username).exists():
                # إرسال رسالة الخطأ
                messages.error(request, f' اسم "{username}" موجود فعلاً! حاولي تضيفي اسم ثنائي 🌸')
                # ضروري جداً تعمل render هنا عشان الرسالة تظهر
                return render(request, 'course/add_user.html', {'form': form})

            # 2. لو الاسم جديد، كمل الكرية عادي
            user = User.objects.create(username=username)
            user.set_unusable_password()
            if role == 'admin':
                user.is_staff = True
                user.is_superuser = True
            user.save()

            messages.success(request, f'تمت إضافة {username} بنجاح! ✅')
            return redirect('dashboard')
    else:
        form = AddUserForm()

    return render(request, 'course/add_user.html', {'form': form})
@staff_member_required
def delete_user(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)
    if not user_to_delete.is_superuser:
        user_to_delete.delete()
    return redirect('dashboard')


@login_required
def student_dashboard(request):
    lessons = Lesson.objects.all().order_by('-created_at')
    my_score = StudentProgress.objects.filter(user=request.user).aggregate(total=Sum('quiz_score'))['total'] or 0

    all_students = User.objects.filter(is_staff=False).annotate(
        total_pts=Sum('studentprogress__quiz_score')
    ).order_by('-total_pts')

    my_rank = "غير محدد"
    for index, student in enumerate(all_students):
        if student == request.user:
            my_rank = index + 1
            break

    return render(request, 'course/student_dashboard.html',
                  {'lessons': lessons, 'my_score': my_score, 'my_rank': my_rank})


@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, 'course/lesson_detail.html', {'lesson': lesson})