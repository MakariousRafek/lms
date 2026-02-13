from django import forms
from .models import Lesson
from django.contrib.auth.models import User


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'video_url', 'video_duration', 'reading_text', 'reading_timer']

        # هنا بندي للـ Inputs كلاسات البوتستراب عشان تطلع شيك من غير تعب
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'رابط الفيديو (يوتيوب)'}),
            'video_duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مدة الفيديو بالدقائق'}),            'reading_text': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'اكتب النص هنا...'}),
            'reading_timer': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مدة التايمر بالدقائق'}),        }

        labels = {
            'title': 'عنوان الدرس',
            'video_url': 'رابط الفيديو',
            'video_duration': 'مدة الفيديو المسموح بها',
            'reading_text': 'نص مرحلة القراءة',
            'reading_timer': 'وقت القراءة',
        }




class AddUserForm(forms.Form):
    username = forms.CharField(
        label='اسم المستخدم',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثال: Mariam_samy'})
    )
    ROLE_CHOICES = [
        ('student', 'طالب (Student)'),
        ('admin', 'مشرف (Admin)')
    ]
    role = forms.ChoiceField(
        label='الصلاحية (Role)',
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
from django import forms
from .models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_type', 'question_text', 'option_1', 'option_2', 'option_3', 'option_4', 'correct_option', 'points']
        widgets = {
            'question_text': forms.Textarea(attrs={'rows': 2, 'placeholder': 'اكتبي نص السؤال هنا..'}),
            # بنخلي الاختيارات تبان بس لو النوع MCQ، ودي بنعملها بالـ CSS أو الـ JS في الصفحة
        }