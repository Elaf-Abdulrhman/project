import os

from django.contrib.auth.forms import AuthenticationForm,User
from .forms import UserSignupForm, AthleteSignupForm, ClubSignupForm, ClubUserSignupForm
from .models import Athlete, Club
from posts.models import Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import logout,login
from .forms import AthleteEditForm ,ClubEditForm
from bookmarks.models import Bookmark
from django.contrib.auth.models import User
from account.forms import AchievementForm


# Create your views here.


def sign_up_as_view(request: HttpRequest):
    if request.user.is_authenticated:
        print(f"User {request.user.username} is logged in.")
    else:
        print("User is NOT logged in.")

    return render(request, "account/sign_up_as.html")


def signup_athlete_view(request):
    if request.method == 'POST':
        user_form = UserSignupForm(request.POST)
        athlete_form = AthleteSignupForm(request.POST, request.FILES)

        if user_form.is_valid() and athlete_form.is_valid():
            user = user_form.save()
            athlete = athlete_form.save(commit=False)
            athlete.user = user
            athlete.save()

            messages.success(request, "Athlete account created successfully! Please log in.")
            return redirect('account:login_view')
        else:
            messages.error(request, "There was an error with your form.")
    else:
        user_form = UserSignupForm()
        athlete_form = AthleteSignupForm()

    return render(request, 'account/signup_athlete.html', {
        'user_form': user_form,
        'athlete_form': athlete_form
    })


def signup_club_view(request):
    if request.method == 'POST':
        user_form = ClubUserSignupForm(request.POST)
        club_form = ClubSignupForm(request.POST, request.FILES)

        if user_form.is_valid() and club_form.is_valid():
            user = user_form.save()
            club = club_form.save(commit=False)
            club.user = user
            club.is_approved = False
            club.save()

            messages.info(request, "Club account created! Awaiting admin approval.")
            return redirect('account:login_view')
        else:

            messages.error(request, "There was an error with your form.")
    else:
        user_form = ClubUserSignupForm()
        club_form = ClubSignupForm()

    return render(request, 'account/signup_club.html', {
        'user_form': user_form,
        'club_form': club_form
    })


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()

            try:
                club = Club.objects.get(user=user)
                if not club.is_approved:
                    messages.error(request, "Club account not approved yet by admin.")
                    return redirect('account:login_view')
            except Club.DoesNotExist:
                pass

            login(request, user)
            if request.user.is_superuser:
                return redirect("admins:dashboard")
            elif hasattr(request.user, 'club'):
                return redirect('account:profile_view', request.user.id)
            else:
                return redirect('posts:all_posts')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'account/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('main:main_page_view')


def profile_view(request: HttpRequest, user_id):
    user = get_object_or_404(User, id=user_id)

    is_bookmarked = (
        Bookmark.objects.filter(user=request.user, profile=user).exists()
        if request.user.is_authenticated else False
    )


    try:
        athlete = Athlete.objects.get(user=user)
        if athlete.isPrivate and request.user != user:
            return render(request, "account/private_profile.html")
    except Athlete.DoesNotExist:
        pass

    context = {
        'user': user,
        'is_bookmarked': is_bookmarked,
        'posts': Post.objects.filter(user=user).order_by('-created_at').distinct(),
    }
    return render(request, "account/profile.html", context)


def edit_profile_athlete_view(request: HttpRequest, user_id):
    athlete = get_object_or_404(Athlete, user__id=user_id)

    if request.method == "POST":
        form = AthleteEditForm(request.POST, request.FILES, instance=athlete, user=athlete.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your athlete profile was updated successfully!")
            return redirect('account:profile_view', user_id=user_id)
    else:
        form = AthleteEditForm(instance=athlete, user=athlete.user)

    return render(request, "account/edit_athlete_profile.html", {"form": form})


def edit_profile_club_view(request: HttpRequest, user_id):
    club = get_object_or_404(Club, user__id=user_id)

    if request.method == "POST":
        form = ClubEditForm(request.POST, request.FILES, instance=club, user=club.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your club profile was updated successfully!")
            return redirect('account:profile_view', user_id=user_id)
    else:
        form = ClubEditForm(instance=club, user=club.user)

    return render(request, "account/edit_club_profile.html", {"form": form})


@login_required
def add_achievement(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Get the user by ID
    athlete = get_object_or_404(Athlete, user=user)  # Get the athlete profile for the user
    if request.method == 'POST':
        form = AchievementForm(request.POST, request.FILES)

        if form.is_valid():
            achievement = form.save(commit=False)
            achievement.user = request.user

            achievement.save()

            return redirect('account:profile_view', user_id=user_id)
    else:
        form = AchievementForm()

    return render(request, 'account/add_achievement.html', {'form': form})



@login_required
def delete_achievement(request, user_id,pk):
    achievement = get_object_or_404(Achievement, pk=pk, user__id=user_id)
    if achievement.user == request.user:
        if request.method == 'POST':
            achievement.delete()
            messages.success(request, "achievement deleted.")
            return redirect('account:profile_view', user_id=user_id)
    else:
        messages.error(request, "You are not authorized to delete this achievement.")
    return render(request, 'account/delete_achievement.html', {'achievement': achievement})