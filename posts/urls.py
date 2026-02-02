from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.all_posts, name='all_posts'),
    path('add/', views.add_post, name='add_post'),
    path('post/<int:post_id>/', views.post_details, name='post_details'),
    path('edit/<int:pk>/', views.edit_post, name='edit_post'),
    path('delete/<int:pk>/', views.delete_post, name='delete_post'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    path('like/<int:post_id>/', views.like_post, name='like_post'),

]
