from django.db import models
from PIL import Image
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    roles_data = ((1,"Admin"), (2, "User"))
    role = models.IntegerField(choices=roles_data, default=1)

class Admin(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True)
    profile_pic = models.FileField(blank=True,null=True, default='default.png', upload_to='avatars/')
    objects = models.Manager()
    def __str__(self):
        return self.user.username

class Client(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True)
    profile_pic = models.FileField(blank=True, null=True, upload_to='avatars/')
    last_login = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return self.user.username

class Category(models.Model):
    category = models.CharField(max_length=100)
    objects = models.Manager()

class File(models.Model):
    file = models.FileField(upload_to='files/')
    Name = models.CharField(max_length=100)
    describe = models.TextField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    thumbnail = models.FileField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    visible = models.BooleanField(default=True)
    objects = models.Manager()
    def __str__(self):
        return self.file.name

