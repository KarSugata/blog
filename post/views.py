from django.shortcuts import render,redirect
from .models import Post, Category, Comment
from django.contrib.auth.models import User
from .forms import CreatePost, CommentForm

# Create your views here.

def home(request): # Home page of the website.
    post = Post.objects.all().order_by('-date_posted') # To display all the post in desc order.
    categories = Category.objects.all()
    
    # categories_count = 0
    '''for item in categories:
        categories_count['item'] = ''
    for item in post:'''
    # categories_count = Post.objects.filter(category=categories).count()
    
    context = {
        'posts':post,
        # 'count' : categories_count,
        'categories': categories,
        # 'categories_count': categories_count
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
                print("Yes valid")
                # form.instance.body = content
                new_comment = form.save(commit=False)
                print(new_comment)
                new_comment.post = post
                new_comment.user = request.user
                new_comment.save()
                return redirect('blog-home')
            
            else:
                print(form.errors)
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
        title = request.POST['title']
        content = request.POST['content']
        # img = request.POST['img']
        print(request.POST)
        # print(form.cleaned_data)
        if form.is_valid():
           
            user = User.objects.get(username=username)
            form.instance.author = user
            form.instance.title = title
            form.instance.content = content
            # form.instance.img = img
            form.save(commit=True)
            return redirect('blog-home')
    else:
        
        form = CreatePost()
    
    context = {
        'form' : form,
        'category': category,
    }
    
    return render(request, 'post/CreatePost1.html',context=context)

def category(request, category_name):
    post_category = Category.objects.get(category=category_name)
    post = post_category.post_set.all()
    context = {
        'posts' : post,
        'category': category_name
    }
    return render(request,'post/CategoryWisePost.html',context=context)

