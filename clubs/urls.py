from django.urls import path
from . import views

app_name = 'clubs'
urlpatterns = [
    path('all/', views.all_clubs, name='all_clubs'),
]
