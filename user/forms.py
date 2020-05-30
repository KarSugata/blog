from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms


class SignUpForm(UserCreationForm):
    class meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class meta:
        model = Profile
        fields = ['user', 'email']
