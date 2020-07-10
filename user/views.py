from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db() # load the profile instance created by the signal
            user.profile.email = form.cleaned_data.get('email')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            print(f'Username: {username}, Password: {password}')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('blog-home')
    else:
        form = SignUpForm()
    
    return render(request, 'user/signup.html', {'form': form})

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

    return render(request, 'user/login.html')

def logoutView(request):
    logout(request)
    return redirect('blog-home')
