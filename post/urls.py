from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('',views.home, name='blog-home'),
    path('post-detail/<int:pk>',views.postdetail, name='post-detail'), # When a post title will be clicked from home.html page
    path('post-category/<str:category_name>',views.category,name='post-category'),
    path('post-list/<str:username>',views.postPerUser, name='post-per-user'),
    path('tag/<slug:tag_slug>/',views.category, name='post_list_by_tag'),
    # Post Create, Update and Delete views url.
    path('create-post/<str:username>',views.createpost,name='create-post'),
    path('delete-post/<int:pk>',views.deletePost, name='delete-post'),
    path('update-post/<int:pk>',views.updatePost, name='update-post'),
    
]
