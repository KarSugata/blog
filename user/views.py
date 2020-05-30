from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
# Create your views here.

def SignUpView(request):
    
    if request.method=='POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
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
        