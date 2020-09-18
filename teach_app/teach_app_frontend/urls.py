from django.urls import path
from teach_app_frontend import views

app_name = 'teach_app_frontend'

#creates url to point to frontend entrypoint
urlpatterns = [
    path('', views.index, name='index'),
]
