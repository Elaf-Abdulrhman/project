from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
from django.db.models import Avg
from account.models import User, Athlete,Club
from posts.models import Post
from bookmarks.models import Bookmark
from django.db.models import Q

def main_page_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("admins:dashboard")
        else:
            return redirect('posts:all_posts')

    athletes = Athlete.objects.filter(isPrivate=False)
    clubs = Club.objects.all()

    latest_posts = Post.objects.filter(
        Q(user__club__isnull=False) |
        Q(user__athlete__isPrivate=False)
    ).order_by('-created_at')[:4]

    bookmarked_post_ids = set()
    if request.user.is_authenticated:
        bookmarked_post_ids = set(
            Bookmark.objects.filter(user=request.user).values_list('post_id', flat=True)
        )

    for post in latest_posts:
        post.is_liked = post.is_liked_by(request.user) if request.user.is_authenticated else False

    return render(request, 'main/main_page.html', {
        "athletes": athletes,
        "clubs": clubs,
        "latest_posts": latest_posts, 
        "bookmarked_post_ids": bookmarked_post_ids,
    })

def about_page_view(request):
    return render(request, 'main/about_us.html')


def mode_view(request:HttpRequest, mode):

    response = redirect(request.GET.get("next", "/"))

    if mode == "light":
        response.set_cookie("mode", "light")
    elif mode == "dark":
        response.set_cookie("mode", "dark")


    return response