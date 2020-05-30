from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile

class SignUpForm(forms.ModelForm):
    class meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

class ProfileForm(UserCreationForm):
    email = forms.EmailField(max_length=200)
    class meta:
        model = Profile
        fields = ['email', 'password1', 'password2']