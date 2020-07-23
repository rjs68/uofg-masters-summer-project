"""teach_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from teach_app_backend import views

urlpatterns = [
    path('', include('teach_app_backend.urls')),
    path('', include('teach_app_frontend.urls')),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('units/', views.get_user_units, name='units'),
    path('create-unit/', views.create_unit, name='create-unit'),
    path('unit-enrol/', views.unit_enrolment, name='unit-enrol'),
    path('assignments/', views.get_user_assignments, name='assignments'),
    path('create-assignment/', views.create_assignment, name='create-assignment'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
