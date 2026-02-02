from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post,Comment,Like,PostImage
from .forms import PostForm,CommentForm
from django.core.paginator import Paginator
from django.db.models import Q
from account.models import Athlete, Club, Sport, City
from django.template.loader import render_to_string
from django.http import JsonResponse
from bookmarks.models import Bookmark
from posts.models import Post, Like





@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')  # multiple images
        video = request.FILES.get('video')        # optional video

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user

            if video:
                post.video = video

            post.save()

            # Save extra uploaded images
            for image in images:
                PostImage.objects.create(post=post, image=image)

            return redirect('posts:post_details', post_id=post.id)
    else:
        form = PostForm()

    return render(request, 'posts/add_post.html', {'form': form})




# def all_posts(request):
#     post_list = Post.objects.all().order_by('-created_at')
#     paginator = Paginator(post_list, 6)
#
#     page_number = request.GET.get('page')
#     posts = paginator.get_page(page_number)
#
#     return render(request, 'posts/all_posts.html', {'posts': posts})


def post_details(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all().order_by('-created_at')  # Fetch related comments

    liked = False
    bookmarked = False  # Initialize bookmarked status

    if request.user.is_authenticated:
        liked = Like.objects.filter(user=request.user, post=post).exists()
        bookmarked = Bookmark.objects.filter(user=request.user, post=post).exists()  # Check if bookmarked

    show_comment_form = request.user.is_authenticated and not request.user.is_superuser

    if request.method == 'POST' and show_comment_form:
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.post = post
                comment.save()
                return redirect('posts:post_details', post_id=post.id)
        else:
            messages.error(request, "You must be logged in to comment.")
            return redirect('account:login_view')
    else:
        form = CommentForm() if show_comment_form else None

    return render(request, 'posts/post_details.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'liked': liked,
        'bookmarked': bookmarked,
    })



@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user != request.user:
        messages.error(request, "You can't delete this comment.")
        return redirect('posts:post_details', post_id=comment.post.id)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Comment deleted.")
        return redirect('posts:post_details', post_id=comment.post.id)

    return redirect('posts:post_details', post_id=comment.post.id)


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user == request.user:
        if request.method == 'POST':
            post.delete()
            messages.success(request, "Post deleted.")
            return redirect('posts:all_posts')
    else:
        messages.error(request, "You are not authorized to delete this post.")
    return render(request, 'posts/delete_post.html', {'post': post})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user:
        messages.error(request, "You are not allowed to edit this post.")
        return redirect('posts:post_details', post_id=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "you updated you post seccessfully!.")
            return redirect('posts:post_details', post_id=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})




@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect(request.META.get('HTTP_REFERER', 'posts:all_posts'))

def all_posts(request):
    sport_id = request.GET.get('sport')
    city_id = request.GET.get('city')
    poster_type = request.GET.get('posted_by')

    filters = Q()
    if sport_id:
        filters &= Q(user__athlete__sport_id=sport_id) | Q(user__club__sport_id=sport_id)
    if city_id:
        filters &= Q(user__athlete__city_id=city_id) | Q(user__club__city_id=city_id)
    if poster_type == 'athlete':
        filters &= Q(user__athlete__isnull=False)
    elif poster_type == 'club':
        filters &= Q(user__club__isnull=False)

    posts = Post.objects.filter(filters).order_by('-created_at').distinct()
    posts = posts.exclude(user__athlete__isPrivate=True)

    # Bookmarks
    bookmarked_post_ids = set()
    if request.user.is_authenticated:
        bookmarked_post_ids = set(
            Bookmark.objects.filter(user=request.user).values_list('post_id', flat=True)
        )

    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Add .is_liked dynamically
    for post in page_obj:
        post.is_liked = post.is_liked_by(request.user) if request.user.is_authenticated else False

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        post_html = render_to_string('posts/post_card.html', {
            'posts': page_obj,
            'bookmarked_post_ids': bookmarked_post_ids,
        }, request=request)
        return JsonResponse({
            'posts_html': post_html,
            'has_next': page_obj.has_next(),
        })

    query_params = request.GET.copy()
    query_params.pop('page', None)
    filter_querystring = query_params.urlencode()

    context = {
        'posts': page_obj,
        'sports': Sport.objects.all(),
        'cities': City.objects.all(),
        'selected_sport': sport_id,
        'selected_city': city_id,
        'selected_poster': poster_type,
        'filter_querystring': filter_querystring,
        'bookmarked_post_ids': bookmarked_post_ids,
    }

    return render(request, 'posts/all_posts.html', context)

    
def latest_posts(request):
    latest_posts = Post.objects.filter(
        user__athlete__isPrivate=False
    ).order_by('-created_at')[:6]

    bookmarked_post_ids = set()
    if request.user.is_authenticated:
        bookmarked_post_ids = set(
            Bookmark.objects.filter(user=request.user).values_list('post_id', flat=True)
        )

    for post in latest_posts:
        post.is_liked = post.is_liked_by(request.user) if request.user.is_authenticated else False

    context = {
        'latest_posts': latest_posts,  # ✅ fixed key
        'bookmarked_post_ids': bookmarked_post_ids,
    }

    return render(request, 'main/main_page.html', context)
