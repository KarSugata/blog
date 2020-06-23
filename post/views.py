from django.shortcuts import render,redirect
from .models import Post, Category, Comment
from django.contrib.auth.models import User
from .forms import CreatePost, CommentForm
from django.contrib import messages
from django.core.paginator import Paginator, Page, PageNotAnInteger, EmptyPage
from taggit.models import Tag
# Create your views here.

def home(request): # Home page of the website.
    post_list = Post.objects.all().order_by('-date_posted') # To display all the post in desc order.
    categories = Category.objects.all()
    # tags = 
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 3)
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'posts':posts,
        'categories': categories,
    }
    
    return render(request,'post/home.html',context=context)

def postdetail(request,pk): # Single Post view.
    
    post = Post.objects.get(id=pk)
    comment = post.comments.all()
    comment_count = comment.count()
    tags = post.tag.all() # retrive all the tags releated to a particular post.

    if request.user.is_authenticated: # Adding the comment adding functionality.

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
        'tags': tags
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
                new_form.save()
                form.save_m2m() # this will help to save the tags in the form.
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
    # print(f'Request Details: {request}')
    user = User.objects.get(username=username) # get all the post specific to th user.
    user_postList = user.post_set.all() # display last 10 posts.
    
    page = request.GET.get('page', 1)
    paginator = Paginator(user_postList, 5)
    
    try:
        user_post = paginator.page(page)
    except PageNotAnInteger:
        user_post = paginator.page(1)
    except EmptyPage:
        user_post = paginator.page(paginator.num_pages)
    
    context = {
        'user_post' :user_post
    }
    
    return render(request, 'post/postPerCategory.html', context=context)

def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    
    if request.method == 'POST':
            post.delete()
            return redirect('blog-home')
    
    context = {
        'post':post
    }

    return render(request, 'blog/DeletePost.html',context=context)

