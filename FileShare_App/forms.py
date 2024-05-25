from django import forms
import os
from pathlib import Path
from .models import Category

def get_categories():
    categories = []
    for category in Category.objects.all():
        categories.append((category.category, category.category))
    return categories

class AddUserForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100, widget = forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password = forms.CharField(label="Password", max_length=100, widget = forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="First Name", max_length=100, widget = forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    last_name = forms.CharField(label="Last Name", max_length=100, widget = forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    profile_pic = forms.ImageField(label="Profile Picture", widget = forms.FileInput(attrs={'class': 'form-control'}))

class addCategoryForm(forms.Form):
    category = forms.CharField(label="Category", widget = forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))

class UploadFileForm(forms.Form):
    file = forms.FileField(label="File", widget = forms.FileInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label="Description", widget = forms.Textarea(attrs={'class': 'form-control'}))
    categories = []
    for category in Category.objects.all().order_by('category'):
        categories.append((category.category, category.category))
    category = forms.ChoiceField(label="Category", choices=categories, widget = forms.Select(attrs={'class': 'form-control'}))






