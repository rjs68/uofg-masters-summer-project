from django.contrib import admin
from teach_app_backend.models import (TeachUser, Unit, UserEnrolledUnit, Assignment, Submission,
                                      Lecture, Quiz, Question, Answer, UserAnswer, UserQuizPerformance)

'''
    Registers database models for admin site with custom columns
'''

@admin.register(TeachUser)
class TeachUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_teacher']


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['unit_code', 'unit_name', 'teacher', 'number_of_credits']


@admin.register(UserEnrolledUnit)
class UserEnrolledUnitAdmin(admin.ModelAdmin):
    list_display = ['user', 'unit']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['unit', 'event_name', 'date_time', 'weight']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'assignment', 'submission_time', 'grade']


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ['unit', 'event_name', 'date_time', 'link']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'question']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'is_correct']


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'answer']


@admin.register(UserQuizPerformance)
class UserQuizPerformanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'grade']


admin.site.register(Quiz)
