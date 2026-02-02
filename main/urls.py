from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.main_page_view, name='main_page_view'),
    path('about/', views.about_page_view, name='about_page_view'),
    path("mode/<mode>/", views.mode_view, name="mode_view"),

]