from django.urls import path
from . import views

app_name = 'bookmarks'  # Define the namespace

urlpatterns = [
    path('bookmark_post/<int:post_id>/', views.bookmark_post, name='bookmark_post'),
    path('all_bookmarks/', views.all_bookmarks, name='all_bookmarks'),
    path('bookmark/profile/<int:profile_id>/', views.bookmark_profile, name='bookmark_profile'),
    path('all_bookmarked_profiles/', views.all_bookmarked_profiles, name='all_bookmarked_profiles'),  # For profile view
]