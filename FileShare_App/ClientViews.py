from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser, Client, File
from django.core.files.storage import FileSystemStorage
import os
from FileSharing import settings
from django.views.decorators.clickjacking import xframe_options_sameorigin, xframe_options_exempt


@login_required
def profile(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    if user.is_superuser:
        context = {'user': user}
        return render(request, 'profile.html', context)
    else:
        client = Client.objects.get(user=user)
        Files = File.objects.filter(uploaded_by=user)
        context = {'user': user, 'client': client, 'user_id': user_id, 'Files': Files}
        return render(request, 'profile.html', context)

def view_file(request, file_id):
    fs = FileSystemStorage()
    file = File.objects.get(id=file_id)
    filename = str(file.file)

    if fs.exists(filename):
        file_path = fs.url(filename)
        context = {'file': file, 'file_path': file_path}
        return render(request, 'ViewPDF.html', context)
    else:
        return HttpResponse('File Not Found')
