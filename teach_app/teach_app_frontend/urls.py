from django.urls import path
from teach_app_frontend import views

app_name = 'teach_app_frontend'

urlpatterns = [
    path('', views.index),
]
