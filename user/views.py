from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, ProfileForm
# Create your views here.

def SignUpView(request):
    
    if request.method == 'POST':
        user_form = SignUpForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST)
        print("hello1")
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_profile = profile_form.save(commit=False)
            print("hello2")
            new_profile.user = new_user
            userName = new_user.username
            password = new_user.password1
            print(f'username: {userName} and password: {password}')
            new_user.save(commit=True)
            new_profile.save(commit=True)
            user = authenticate(username = userName, password = password)
            print(f'user: {user}')
            login(request, user)
            return redirect('blog-home')
    else:
        user_form = SignUpForm()
        profile_form = ProfileForm()
    
    context = {
        'user_form': user_form, 
        'profile_form': profile_form,
    }

    return render(request, 'user/signup.html', context=context)

def loginView(request):
    
    if request.method == 'POST':
        userName = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=userName, password=password)
        
        if user is not  None:
            login(request, user)
            return redirect('blog-home')
        
        else :
            print("Not allowed")

    return render(request, 'user/login.html',)

def logoutView(request):
    logout(request)
    return redirect('blog-home')