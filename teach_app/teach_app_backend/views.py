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
        data = json.loads(request.body)
        # Retrieves username and password
        email = data['email']
        password = data['password']
        # Authenticates the user
        user = authenticate(request, email=email, password=password)
        print(user)

        if user:
            print("Yeaaa boiiiii")
            if user.is_active:
                # If valid, log in the user
                login(request, user)
                return HttpResponse("Login Successful")
        else:
            print("Not quite")
            # If there are any authentication errors, send error feedback
            loginFeedback = json.dumps({
                "error": "Invalid credentials"
            })
            context = {'loginFeedback': loginFeedback}
            # return render(request, 'login.html', context=context)
            return HttpResponse("Login Unsuccessful")
    else:
        return HttpResponse("Not a post request")
