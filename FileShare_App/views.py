from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from pathlib import Path
from django.contrib.auth.decorators import login_required
from .models import Client
import os

# Create your views here.
def get_categories():
    dir_path = Path(__file__).resolve().parent.parent / 'media' / 'documents'
    categories = []
    for file in os.listdir(dir_path):
        if os.path.isdir(os.path.join(dir_path, file)):
            categories.append(file)
    return categories


def home(request):
    categories = get_categories()
    return render(request, 'home.html', {'categories': categories})

def dologin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            client = Client.objects.get(user=user)
            client.last_login = datetime.now()
            client.save()
            messages.success(request, 'Login Successful!')
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Login Failed! Please try again.')
            return HttpResponseRedirect('/')

def dologout(request):
    logout(request)
    return HttpResponseRedirect('/')
@login_required
def test(request):
    print(Path(__file__).resolve().parent.parent.parent)
    return render(request, 'Login.html')