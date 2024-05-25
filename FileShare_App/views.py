from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from pathlib import Path
from django.contrib.auth.decorators import login_required
from .models import Client, File, Category, CustomUser
import os
from django.core import serializers
from django.http import HttpResponse
from json import dumps

# Create your views here.
def get_categories():
    dir_path = Path(__file__).resolve().parent.parent / 'media'
    categories = []
    for file in os.listdir(dir_path):
        if os.path.isdir(os.path.join(dir_path, file)):
            categories.append(file)
    return categories


def home(request, *page):
    Files = File.objects.filter(visible=True).order_by('-uploaded_at')[:12]
    NumberOfFiles = range(1,int(File.objects.all().count()//12)+2)
    print(NumberOfFiles)
    FileName = list(File.objects.values_list('Name', flat=True))
    file_list = []
    for file in File.objects.all():
        file_dict = {
            'ID': file.id,
            'Name': file.Name,
        }
        file_list.append(file_dict)
    jsonfile = dumps(file_list)
    print(jsonfile)
    context = {'Files': Files, 'NumberOfFiles': NumberOfFiles, 'FileName': FileName, 'jsonfile': jsonfile}
    return render(request, 'home.html', context)

def dologin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                messages.success(request, 'Admin Login Successful!')
                return HttpResponseRedirect('/')
            else:
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

def test(request):
    Users = CustomUser.objects.all()
    jsonfile = serializers.serialize('json', Users)
    return HttpResponse(jsonfile,content_type='application/json')

def list_files(request):
    Files = File.objects.all()[:8]
    print(Files)
    return render(request, 'Login.html', {'Files': Files})

def filter_files(request, category):
    Files = File.objects.filter(category=Category.objects.get(category=category), visible=True).order_by('-uploaded_at')[:12]
    return render(request, 'Home.html', {'Files': Files})

def page(request, page):
    page -= 1
    Files = File.objects.filter(visible = True).order_by('-uploaded_at')[int(page)*12:int(page)*12+12]
    NumberOfFiles = range(1, int(File.objects.all().count() // 12) + 2)
    return render(request, 'Home.html', {'Files': Files, 'NumberOfFiles': NumberOfFiles})