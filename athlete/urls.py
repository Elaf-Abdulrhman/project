from django.urls import path
from . import views

app_name = 'athlete'
urlpatterns = [
    path('all/', views.all_athletes, name='all_athletes'),
]
