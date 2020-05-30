from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
# Create your views here.

def SignUpView(request):
    
    if request.method=='POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user.profile.email = form.cleaned_data.get('email')
            user.save()
            print(f'Password: {password} and Username: {username} and email: {email}')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('blog-home')
    else:
    
        form = SignUpForm()

    context = {'form':form}
    
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
        