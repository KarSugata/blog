from django.shortcuts import render,redirect
from .models import Post, Category, Comment
from django.contrib.auth.models import User
from .forms import CreatePost, CommentForm
from django.contrib import messages
# Create your views here.

def home(request): # Home page of the website.
    post = Post.objects.all().order_by('-date_posted') # To display all the post in desc order.
    categories = Category.objects.all()
    
    context = {
        'posts':post,
        'categories': categories,
    }
    
    return render(request,'post/home.html',context=context)

def postdetail(request,pk): # Single Post view.
    
    post = Post.objects.get(id=pk)
    comment = post.comments.all()
    comment_count = comment.count()
    
    if request.user.is_authenticated:

        if request.method == 'POST':
            form = CommentForm(data=request.POST)
            
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.post = post
                new_comment.user = request.user
                new_comment.save()
            
            else:
                pass
        else:
            form = CommentForm()

    context = {
        'comment_form': CommentForm,
        'post' : post,
        'comments': comment,
        'count': comment_count,
    }

    return render(request,'post/postdetail.html', context=context)

def createpost(request,username):
    
    if request.method == 'POST':
        form = CreatePost(request.POST, request.FILES)
        if form.is_valid():
            
            new_form = form.save(commit=False)
            user = User.objects.get(username=username)
            
            if user.post_set.filter(title=new_form.title).exists(): # if the post exist with the same title under the same author do not add the post.
                messages.error(request, 'Blog already present with the same title')
            
            else:
                new_form.author = user
                form.save(commit=True)
                messages.success(request, 'Blog posted successfully')
                return redirect('blog-home')
        
        else:
            messages.error(request, 'Form not valid! Try again')
    
    else:
        
        form = CreatePost()
    
    context = {
        'form' : form,
        'category': category,
    }
    
    return render(request, 'post/CreatePost.html',context=context)

def category(request, category_name):
    post_category = Category.objects.get(category=category_name)
    post = post_category.post_set.all()
    context = {
        'posts' : post,
        'category': category_name
    }
    return render(request,'post/CategoryWisePost.html',context=context)

def postPerUser(request, username):
    user = User.objects.get(username=username)
    user_post = user.post_set.all()[:10]
    
    context = {
        'user_post' :user_post
    }
    
    return render(request, 'post/postPerCategory.html', context=context)