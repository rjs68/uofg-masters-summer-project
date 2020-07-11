from django.urls import path
from teach_app_backend import views

app_name = 'teach'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/teach_user', views.TeachUserListCreate.as_view()),
]
