from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('',views.home, name='blog-home'),
    path('post-detail/<int:pk>',views.postdetail, name='post-detail'), # When a post title will be clicked from home.html page
    path('create-post/<str:username>',views.createpost,name='create-post'),
    path('post-category/<str:category_name>',views.category,name='post-category'),

]
