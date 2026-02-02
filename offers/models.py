from django.db import models
from django.contrib.auth.models import User

class Offer(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('A', 'All'),
    ]


    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    photo = models.ImageField(upload_to='posts/photos/', blank=True, null=True)

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='A')


    email = models.EmailField(blank=True)
    url = models.URLField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)


def __str__(self):
        return self.title



class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    offer = models.ForeignKey('Offer', on_delete=models.CASCADE, related_name='applications')
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    response_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('offer', 'athlete')

    def __str__(self):
        return f"{self.athlete.username} applied to {self.offer.title} ({self.status})"
