from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('payment/', views.payment, name='payment'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('plus_plan/', views.plus_plan, name='plus_plan'),
]
