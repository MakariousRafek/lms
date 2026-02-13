from django.contrib import admin
from .models import Lesson, Question, StudentProgress

# This makes the Question interface show up inside the Lesson page!
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('title', 'video_duration', 'reading_timer')

admin.site.register(Lesson, LessonAdmin)
admin.site.register(StudentProgress)