from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Category(models.Model):
    
    CATEGORY = (
        ("Un-categorized", "Un-categorized"),
        ("Machine Learning", "Machine Learning"),
        ("Data Science", "Data Science"),
        ("Programming", "Programming"),
        ("Latest Trends", "Latest Trends")
    )
    
    category = models.CharField(max_length=20, choices=CATEGORY, default='Un-Categorized',unique=True)

    def __str__(self):
        return self.category

class Post(models.Model):
    
    title = models.CharField(max_length=20) # title of the post
    content = models.TextField()  # content of the post
    date_posted = models.DateTimeField(auto_now_add=True)  # when the post is created
    date_modified = models.DateTimeField(auto_now=True) # will store the date every time the post is updated and saved.
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Referring the django's inbuilt User model.
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # one post can have only one category whereas under one category there can be multiple post.
    img = models.ImageField(default='default.jpg', upload_to='post')
    # tag = to store important tags related to the post
    # date_updated = when the blog is updated

    def __str__(self):
        return self.title

class Comment(models.Model):
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('created',)
    
