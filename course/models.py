from django.db import models
from django.contrib.auth.models import User
import re


# ==========================================
# 1. موديل الدرس / المسابقة
# ==========================================
class Lesson(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان المسابقة/الدرس")
    video_url = models.URLField(verbose_name="رابط فيديو يوتيوب")
    video_duration = models.IntegerField(verbose_name="مدة الفيديو (بالدقائق)")
    reading_text = models.TextField(verbose_name="نص مرحلة القراءة")
    reading_timer = models.IntegerField(verbose_name="وقت القراءة (بالدقائق)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")

    def __str__(self):
        return self.title

    def get_embed_url(self):
        """دالة ذكية لتحويل أي رابط يوتيوب لصيغة الـ Embed عشان يشتغل في الـ iframe"""
        regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})"
        match = re.search(regex, self.video_url)
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/embed/{video_id}"
        return self.video_url


# ==========================================
# 2. موديل الأسئلة (دعم المقالي والاختياري)
# ==========================================
class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='questions',
                               verbose_name="الدرس التابع له")

    TYPE_CHOICES = [
        ('mcq', 'اختيار من متعدد'),
        ('text', 'سؤال مقالي')
    ]
    question_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='mcq', verbose_name="نوع السؤال")

    question_text = models.CharField(max_length=500, verbose_name="نص السؤال")

    # حقول الاختيارات (للمتعدد فقط)
    option_1 = models.CharField(max_length=200, blank=True, null=True, verbose_name="الاختيار 1")
    option_2 = models.CharField(max_length=200, blank=True, null=True, verbose_name="الاختيار 2")
    option_3 = models.CharField(max_length=200, blank=True, null=True, verbose_name="الاختيار 3")
    option_4 = models.CharField(max_length=200, blank=True, null=True, verbose_name="الاختيار 4")

    CORRECT_CHOICES = [(1, '1'), (2, '2'), (3, '3'), (4, '4')]
    correct_option = models.IntegerField(choices=CORRECT_CHOICES, blank=True, null=True, verbose_name="الإجابة الصح")

    # النقاط اللي تاسوني بتحددها لكل سؤال
    points = models.IntegerField(default=1, verbose_name="النقاط")

    def __str__(self):
        return f"{self.question_text[:30]}"


# ==========================================
# 3. موديل تقدم الطالبة
# ==========================================
class StudentProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='studentprogress', verbose_name="الطالبة")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress', verbose_name="المسابقة")

    # الدرجة الإجمالية (MCQ + المقالي المتصحح)
    quiz_score = models.IntegerField(default=0, verbose_name="إجمالي السكور")
    is_completed = models.BooleanField(default=False, verbose_name="تم الحل")
    date_completed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"


# ==========================================
# 4. موديل إجابات المقالي (للتصحيح اليدوي)
# ==========================================
class EssayAnswer(models.Model):
    progress = models.ForeignKey(StudentProgress, on_delete=models.CASCADE, related_name='essay_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(verbose_name="إجابة الطالبة")

    # الدرجة اللي تاسوني بتحطها بعد ما تقرأ
    points_earned = models.IntegerField(default=0, verbose_name="الدرجة اللي خدتها")
    is_graded = models.BooleanField(default=False, verbose_name="اتصححت؟")

    def __str__(self):
        return f"مقالي: {self.progress.user.username}"