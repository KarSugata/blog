from .models import Post,Comment
# from django.forms import ModelForm
from django import forms

class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'img']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']