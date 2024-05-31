"""
URL configuration for FileSharing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views. home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from FileShare_App import views, AdminViews, ClientViews
from . import settings
from django.conf.urls.static import static
urlpatterns = ([
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.dologin, name='login'),
    path('logout/', views.dologout, name='logout'),
    path('test/', views.test, name='test'),
    #Admin Views
    path('Register/', AdminViews.AddUser, name='Register'),
    path('AddUser/', AdminViews.AddUserSubmit, name='SaveUser'),
    path('UploadFile/', AdminViews.UploadFile, name='UploadFile'),
    path('Filesave/', AdminViews.Filesave, name='Filesave'),
    path('manage_users/', AdminViews.manage_accounts, name='manage_users'),
    path('delete_user/<str:user_id>/', AdminViews.del_account, name='delete_user'),
    #Client Views
    path('Profile/<str:user_id>/', ClientViews.profile, name='Profile'),
    path('ViewFiles/<int:file_id>', ClientViews.view_file, name='ViewFiles'),
    path('list_files/', views.list_files, name='list_files'),
    path('AddCategory/', AdminViews.AddCategory, name='AddCategory'),
    path('category/<str:category>/', views.filter_files, name='filter_files'),
    path('page/<int:page>/', views.page, name='page_list'),
    path('manage_files/', AdminViews.manage_files, name='manage_files'),
    path('delete_file/<int:file_id>/', AdminViews.delete_file, name='delete_file'),
    path('change_status/<int:file_id>/', AdminViews.change_status, name='change_status'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
