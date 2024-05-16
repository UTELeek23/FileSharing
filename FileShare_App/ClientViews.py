from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser, Client, File
from django.core.files.storage import FileSystemStorage


@login_required
def profile(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    client = Client.objects.get(user=user)
    Files = File.objects.filter(uploaded_by=client)
    context = {'user': user, 'client': client, 'user_id': user_id, 'Files': Files}
    return render(request, 'profile.html', context)


def view_file(request, category ,file_id):
    print("ok")
    fs = FileSystemStorage(location='media/documents/' + category)
    file = File.objects.get(id=file_id)
    filename = str(file.file)
    print(filename)
    if fs.exists(filename):
        with fs.open(filename) as f:
            response = HttpResponse(f, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename=' + filename
            return response
    else:
        return HttpResponse('File Not Found')