from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Athlete, Club,Achievement




class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class ClubUserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AthleteSignupForm(forms.ModelForm):
    class Meta:
        model = Athlete
        exclude = ['user']

class ClubSignupForm(forms.ModelForm):
    class Meta:
        model = Club
        exclude = ['user', 'is_approved']


class AthleteEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = Athlete
        fields = [
            'profilePhoto', 'phoneNumber', 'dateOfBirth', 'sport', 'playingPosition',
            'height', 'weight', 'gender', 'isAvailable', 'isPrivate', 'city',
            'bio', 'facebook', 'twitterX', 'instagram'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'dateOfBirth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['username'].initial = self.user.username
            self.fields['email'].initial = self.user.email

    def save(self, commit=True):
        athlete = super().save(commit=False)
        if self.user:
            user = athlete.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
        if commit:
            athlete.save()
        return athlete
class ClubEditForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = Club
        fields = [
            'photo', 'clubName', 'phoneNumber', 'sport', 'city',
            'description', 'facebook', 'twitterX', 'instagram'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['username'].initial = self.user.username
            self.fields['email'].initial = self.user.email

    def save(self, commit=True):
        club = super().save(commit=False)
        if self.user:
            user = club.user
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
        if commit:
            club.save()
        return club

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = [ 'title','dateOfStart','dateOfEnd','content', 'file']