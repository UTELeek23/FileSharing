from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from pathlib import Path
from .forms import *
from django.core.files.storage import FileSystemStorage
from .models import CustomUser, Client, File
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .pdf2img import pdf2img
from FileSharing import settings
import logging
from django.shortcuts import get_object_or_404, redirect

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


logger = logging.getLogger(__name__)
@login_required
def Filesave(request):
    if request.method != 'POST':
        return HttpResponse('Invalid Request')
    else:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            fs = FileSystemStorage()
            if 'pdf' not in file.content_type:
                messages.error(request, 'Only PDF files are allowed!')
                return render(request, 'UploadFile.html', {'form': form})
            tmp_name = str(hash(file.name.encode('utf-8'))) + '.pdf'
            # print(tmpname)
            filename = fs.save(tmp_name, file)
            file_url = fs.url(filename)
            print(file_url)
            imgname = pdf2img('media/' + tmp_name, 'static/Media/', tmp_name.replace('.pdf', ''))
            try:
                file = File(file=filename, Name=file.name, describe=description, category=Category.objects.get(category=category),
                            uploaded_by=CustomUser.objects.get(id=request.user.id), thumbnail = imgname)
                file.save()
                messages.success(request, 'File Uploaded Successfully')
                return HttpResponseRedirect('/UploadFile')
            except:
                messages.error(request, 'File Upload Failed')
                return HttpResponseRedirect(reversed('UploadFile'))
        else:
            messages.error(request, 'Invalid Form')
            return render(request, 'UploadFile.html', {'form': form})
@login_required
def AddCategory(request):
    if request.method != 'POST':
        return HttpResponse('Invalid Request')
    else:
        category = request.POST['Category']
        print(type(category))
        try:
           List_category = Category.objects.all()
           List_category = [i.category for i in List_category]
           if category in List_category:
                messages.error(request, 'Category Already Exists')
                return HttpResponseRedirect('/Profile/' + str(request.user.id))
           else:
                category = Category(category=category)
                category.save()
                messages.success(request, 'Category Added Successfully')
                return HttpResponseRedirect('/Profile/' + str(request.user.id))
        except:
            messages.error(request, 'Category Addition Failed')
            return HttpResponseRedirect('/Profile/' + str(request.user.id))
@login_required
def manage_files(request):
    Files = File.objects.all()
    users = CustomUser.objects.all()
    return render(request, 'manage_files.html', {'Files': Files, 'users': users})
@login_required
def change_status(request, file_id):
    file = File.objects.get(id=file_id)
    file.visible = not file.visible
    file.save()
    return HttpResponseRedirect('/manage_files')
@login_required
def delete_file(request, file_id):
    user = CustomUser.objects.get(id=request.user.id)
    if user.is_superuser:
        file = File.objects.get(id=file_id)
        path_file = os.path.join(settings.MEDIA_ROOT, file.file.name)
        if os.path.isfile(path_file):
            os.remove(path_file)
        path_thumbnail = os.path.join(settings.STATIC_URL, 'Media', str(file.thumbnail))
        print(path_thumbnail)
        if os.path.isfile(path_thumbnail):
            os.remove(path_thumbnail)
        file.delete()
        return HttpResponseRedirect('/manage_files')
    else:
        file = File.objects.get(id=file_id)
        if file.uploaded_by == user:
            path_file = os.path.join(settings.MEDIA_ROOT, file.file.name)
            if os.path.isfile(path_file):
                os.remove(path_file)
            path_thumbnail = os.path.join(settings.STATIC_URL, 'Media', str(file.thumbnail))
            print(path_thumbnail)
            if os.path.isfile(path_thumbnail):
                os.remove(path_thumbnail)
            file.delete()
            return HttpResponseRedirect('/Profile/' + str(request.user.id))
        else:
            return HttpResponseRedirect('/manage_files')
    return HttpResponseRedirect('/manage_files')

@login_required
def manage_accounts(request):
    users = CustomUser.objects.all()
    return render(request, 'manage_accounts.html', {'users': users})

@login_required
def del_account(request, user_id):
    # Ensure the user is authenticated and has permission to delete the account
    if not request.user.is_authenticated or not request.user.has_perm('auth.delete_user'):
        return HttpResponseForbidden("You do not have permission to delete this account.")

    user = get_object_or_404(CustomUser, id=user_id)
    client = get_object_or_404(Client, user=user)
    files = File.objects.filter(uploaded_by=user)
    try:
        if client.profile_pic:
            profile_pic_path = os.path.join(settings.MEDIA_ROOT, 'avatars', str(client.profile_pic.name))
            if os.path.isfile(profile_pic_path):
                os.remove(profile_pic_path)
        for file in files:
            file_path = os.path.join(settings.MEDIA_ROOT, file.file.name)
            if os.path.isfile(file_path):
                os.remove(file_path)
            thumbnail_path = os.path.join(settings.STATIC_URL, 'Media', str(file.thumbnail))
            if os.path.isfile(thumbnail_path):
                os.remove(thumbnail_path)
            file.delete()
        user.delete()

        # Log the account deletion
        logger.info(f"User {user_id} and associated client data deleted successfully.")
        messages.success(request, 'User deleted successfully.')

    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        return HttpResponseForbidden("An error occurred while deleting the account.")

    return redirect('/')