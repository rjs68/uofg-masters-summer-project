from django.shortcuts import render

from django.http import HttpResponse
from rest_framework import generics

from teach_app_backend.models import TeachUser
from teach_app_backend.serializers import TeachUserSerializer


def index(request):
    return HttpResponse("Welcome to Teach")


class TeachUserListCreate(generics.ListCreateAPIView):
    queryset = TeachUser.objects.all()
    serializer_class = TeachUserSerializer

