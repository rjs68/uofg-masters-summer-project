from django.urls import path
from teach_app_backend import views

app_name = 'teach'

urlpatterns = [
    path('', views.index, name='index'),
]
