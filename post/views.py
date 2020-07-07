from django.shortcuts import render,redirect, get_object_or_404, reverse, HttpResponseRedirect
from .models import Post, Category, Comment
from django.contrib.auth.models import User
from .forms import CreatePost, CommentForm, UpdateForm
from django.contrib import messages
from django.core.paginator import Paginator, Page, PageNotAnInteger, EmptyPage
from taggit.models import Tag
# Create your views here.

def home(request): # Home page of the website.
    post_list = Post.objects.all().order_by('-date_posted') # To display all the post in desc order.
    categories = Category.objects.all() # getting all the objects of categories.
    tags = Post.tag.most_common()[:6] # getting the 6 most common post tags.
    
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 3) # creating a Paginator object. Each page will consist of 3 pages.
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'posts':posts,
        'categories': categories,
        'tags':tags,
    }
    
    return render(request,'post/home.html',context=context)

def postdetail(request, pk): # Single Post view.
    
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
                return HttpResponseRedirect(reverse('post-detail', args=[pk]))
            
            else:
                pass
        else:
            form = CommentForm()

    context = {
        'comment_form': CommentForm,
        'post' : post,
        'comments': comment,
        'count': comment_count,
        'tags': tags,
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

def category(request, category_name=None, tag_slug=None):
    
    if category_name: # if the view is handling all the post under a particular category.
        post_category = Category.objects.get(category=category_name)
        post = post_category.post_set.all()
    
    tag = None
    
    if tag_slug: # if the view is handling all the post under a particular tag.
        post = Post.objects.all() # retrive all the post.
        tag = get_object_or_404(Tag, slug=tag_slug)
        post = post.filter(tag__in=[tag]) # retrive all the post under a particular tag.
        
    context = {
        'posts' : post,
        'category': category_name,
        'tag' : tag,
    }
    return render(request,'post/CategoryWisePost.html',context=context)

def postPerUser(request, username):

    user = User.objects.get(username=username) # get all the post specific to the user.
    user_postList = user.post_set.all().order_by('date_posted') # display last 10 posts.
    
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
    
    return render(request, 'post/deletePost.html')

def updatePost(request, pk):
    
    post = Post.objects.get(id=pk)

    if request.method == 'POST':
        if request.user == post.author:
            form = UpdateForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('post-detail', pk=pk)
        else:
            print("You are not authorized!")
    else:
        form = UpdateForm(instance=post)

    context = {
        'form':form
    }

    return render(request, 'post/UpdatePost.html',context=context)
