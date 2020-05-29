from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def SignUpView(request):
    # if request.method == 'POST':

    context = {}
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
        