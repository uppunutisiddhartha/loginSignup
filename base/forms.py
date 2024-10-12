# base/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, Book

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['firstname', 'lastname', 'mail', 'photo']
        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'mail': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'image', 'category', 'selected_item', 'pdf']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter author name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter book description'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'selected_item': forms.Select(attrs={'class': 'form-control'}),
            'pdf': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
