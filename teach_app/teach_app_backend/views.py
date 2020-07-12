import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import generics

from teach_app_backend.models import TeachUser
from teach_app_backend.serializers import TeachUserSerializer


def index(request):
    return HttpResponse("Welcome to Teach")


class TeachUserListCreate(generics.ListCreateAPIView):
    queryset = TeachUser.objects.all()
    serializer_class = TeachUserSerializer


def user_login(request):
    if request.method == 'POST':
        # Retrieves username and password
        email = request.POST['email']
        password = request.POST['password']
        # Authenticates the user
        user = authenticate(request, email=email, password=password)

        if user:
            if user.is_active:
                # If valid, log in the user
                login(request, user)
                return HttpResponse("Successfully logged in")
        else:
            # If there are any authentication errors, send error feedback
            login_feedback = json.dumps({
                "error": "Invalid credentials"
            })
            context = {'loginFeedback': login_feedback}
            return render(request, 'login.html', context=context)
    else:
        return render(request, 'login.html')
