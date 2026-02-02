from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from .models import Bookmark
from posts.models import Post
from django.contrib.auth.models import User

@login_required
def bookmark_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)

    if not created:
        # If the bookmark already exists, remove it
        bookmark.delete()

    return redirect(request.META.get('HTTP_REFERER', 'posts:all_posts'))
@login_required
def all_bookmarks(request):
    # Filter bookmarks for the logged-in user
    bookmarks = Bookmark.objects.filter(user=request.user, post__isnull=False).select_related('post')
    liked_posts = Post.objects.filter(likes__user=request.user)  # Posts liked by the user
    bookmarked_posts = Post.objects.filter(bookmarked_by__user=request.user)  # Posts bookmarked by the user

    # Handle infinite scrolling
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        offset = int(request.GET.get('offset', 0))  # Starting point
        limit = int(request.GET.get('limit', 2))    # Number of items to load
        sliced_bookmarks = bookmarks[offset:offset + limit]

        posts_html = render(request, 'bookmarks/bookmarked_post_card.html', {
            'bookmarks': sliced_bookmarks,
            'liked_posts': liked_posts,
            'bookmarked_posts': bookmarked_posts,
        }).content.decode('utf-8')
        return JsonResponse({
            'posts_html': posts_html,
            'has_next': len(bookmarks) > offset + limit,  # Check if there are more items
        })

    # Render the full page for non-AJAX requests
    return render(request, 'bookmarks/all_bookmarks.html', {
        'bookmarks': bookmarks,
        'liked_posts': liked_posts,
        'bookmarked_posts': bookmarked_posts,
    })

@login_required
def bookmark_profile(request, profile_id):
    profile = get_object_or_404(User, id=profile_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, profile=profile)

    if not created:
        # If the bookmark already exists, remove it
        bookmark.delete()

    # Redirect back to the profile page
    return redirect('account:profile_view', user_id=profile.id)

@login_required
def all_bookmarked_profiles(request):
    bookmarks = Bookmark.objects.filter(user=request.user, profile__isnull=False)
    return render(request, 'bookmarks/all_bookmarked_profiles.html', {'bookmarks': bookmarks})