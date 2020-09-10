from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from teach_app_backend import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', include('teach_app_backend.urls')),
    path('', include('teach_app_frontend.urls')),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('units/', views.get_user_units, name='units'),
    path('create-unit/', views.create_unit, name='create-unit'),
    path('unit-enrol/', views.unit_enrolment, name='unit-enrol'),
    path('lectures/', views.get_user_lectures, name='lectures'),
    path('create-lecture/', views.create_lecture, name='create-lecture'),
    path('assignments/', views.get_user_assignments, name='assignments'),
    path('create-assignment/', views.create_assignment, name='create-assignment'),
    path('assignment-specification/', views.get_assignment_specification, name='assignment-specification'),
    path('specification-name/', views.get_assignment_specification_name, name='specification name'),
    path('upload-specification/', views.upload_assignment_specification, name='upload-specification'),
    path('submission/', views.get_submission, name='submission'),
    path('submission-name/', views.get_submission_name, name='submission-name'),
    path('upload-submission/', views.upload_submission, name='upload-submission'),
    path('student-submissions/', views.get_student_submissions, name='student-submissions'),
    path('student-grade/', views.edit_student_grade, name='student-grade'),
    path('student-feedback/', views.edit_student_feedback, name='student-feedback'),
    path('quiz/', views.get_quiz, name='quiz'),
    path('submit-answer/', views.submit_user_answer, name='submit-answer'),
    path('quiz-results/', views.get_quiz_results, name='quiz-results'),
    path('admin/', admin.site.urls),
    path('favicon.ico/', RedirectView.as_view(url='/teach_app_frontend/static/frontend/favicon.ico/'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
