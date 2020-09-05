import json

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse

def index(request):
    return render(request, 'frontend/index.html')
