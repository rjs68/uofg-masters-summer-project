import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import generics

from teach_app_backend.models import TeachUser, University
from teach_app_backend.serializers import TeachUserSerializer
from populate_teach import add_user


def index(request):
    return HttpResponse("Welcome to Teach")


class TeachUserListCreate(generics.ListCreateAPIView):
    queryset = TeachUser.objects.all()
    serializer_class = TeachUserSerializer


def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Retrieves username and password
        email = data['email']
        password = data['password']
        # Authenticates the user
        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            return HttpResponse("Login Successful")
        else:
            # If there are any authentication errors, send error feedback
            return HttpResponse("Login Unsuccessful", status=401)
    else:
        return HttpResponse("Not a valid request")


def user_signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        enrol_key = data['enrolmentKey']

        university = None
        is_teacher = None
        try:
            university = University.objects.get(teacher_enrol_key=enrol_key)
            is_teacher = True
        except:
            try:
                university = University.objects.get(student_enrol_key=enrol_key)
                is_teacher = False
            except:
                return HttpResponse("Invalid Enrolment Key", status=401)
        
        email = data['email']
        password = data['password']
        first_name = data['firstName']
        last_name = data['lastName']
        university_name = university.university_name

        user = add_user(email, password, first_name, last_name, university_name, is_teacher)

        if user:
            print("user added")
            login(request, user)
            return HttpResponse("User Creation Successful")
        else:
            print("user not added")
            # If there are any authentication errors, send error feedback
            return HttpResponse("User Creation Unsuccessful", status=401)
    else:
        return HttpResponse("Not a valid request")
