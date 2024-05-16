from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from pathlib import Path
from .forms import *
from django.core.files.storage import FileSystemStorage
from .models import CustomUser, Client
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@login_required
def AddUser(request):
    form = AddUserForm()
    return render(request, 'Add_user.html', {'form': form})
@csrf_exempt
def AddUserSubmit(request):
    if request.method != 'POST':
        return HttpResponse('Invalid Request')
    else:
        form = AddUserForm(request.POST, request.FILES)
        if form.is_valid():
            firstname = form.cleaned_data['first_name']
            lastname = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage(location='media/avatars')
            filename = fs.save(profile_pic.name, profile_pic)
            print(username, password, firstname, lastname, filename)
            print(profile_pic.name)
            try:
                user = CustomUser.objects.create_user(username=username, password=password, first_name=firstname, last_name=lastname, role=2)
                client = Client(user=user, profile_pic=filename)
                user.save()
                client.save()
                messages.success(request, 'User Added Successfully')
                return HttpResponseRedirect('/')
            except:
                messages.error(request, 'User Addition Failed')
                return HttpResponseRedirect(reversed('Register'))
        else:
            messages.error(request, 'Invalid Form')
            return render(request, 'Add_user.html', {'form': form})

@login_required
def UploadFile(request):
    form = UploadFileForm()
    return render(request, 'UploadFile.html', {'form': form})

def Filesave(request):
    if request.method != 'POST':
        return HttpResponse('Invalid Request')
    else:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            fs = FileSystemStorage(location='media/' + 'documents/' + category)
            if 'pdf' not in file.content_type:
                messages.error(request, 'Only PDF files are allowed!')
                return render(request, 'UploadFile.html', {'form': form})
            tmp_name = str(file.name.encode('utf-8').hex())
            # print(tmpname)
            filename = fs.save(tmp_name, file)
            try:
                file = File(file=filename, Name=file.name, describe=description, category=category,
                            uploaded_by=Client.objects.get(user=request.user.id))
                file.save()
                messages.success(request, 'File Uploaded Successfully')
                return HttpResponseRedirect('/UploadFile')
            except:
                messages.error(request, 'File Upload Failed')
                return HttpResponseRedirect(reversed('UploadFile'))
        else:
            messages.error(request, 'Invalid Form')
            return render(request, 'UploadFile.html', {'form': form})