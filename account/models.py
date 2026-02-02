from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class City(models.Model):
    city_name= models.CharField(max_length=50)
    def __str__(self):
        return self.city_name

    
    
class Sport(models.Model):
    sport_name=models.CharField(max_length=50)
    def __str__(self):
        return self.sport_name

class Athlete(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    sport = models.ForeignKey(Sport, on_delete=models.SET_NULL, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phoneNumber = models.CharField(max_length=15)
    playingPosition = models.CharField(max_length=100)
    height = models.FloatField()
    weight = models.FloatField()
    dateOfBirth = models.DateTimeField()
    profilePhoto = models.ImageField(upload_to='athletes/photos/', default="static/images/profile.png")
    bio = models.TextField(blank=True) 
    isAvailable = models.BooleanField(default=True)
    isPrivate = models.BooleanField(default=False)
    facebook = models.URLField(blank=True)
    twitterX = models.URLField(blank=True)
    instagram = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username} - Athlete"

class Club(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    sport = models.ForeignKey(Sport, on_delete=models.SET_NULL, null=True)
    clubName = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='media/clubs/photos/', default="static/images/profile.png")
    description = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    facebook = models.URLField(blank=True)
    twitterX = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    def __str__(self):
        return f"{self.clubName} ({'Approved' if self.is_approved else 'Pending'})"

class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150,blank=True)
    dateOfStart = models.DateTimeField()
    dateOfEnd = models.DateTimeField()
    content= models.TextField(blank=True) 
    file = models.ImageField(upload_to='athletes/photos/')

