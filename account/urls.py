from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy



app_name="account"

urlpatterns = [
    
    path("signup/", views.sign_up_as_view,name="sign_up_as_view"),
    path("profile/<int:user_id>/", views.profile_view,name="profile_view"),
    path("signup/as/athlete/", views.signup_athlete_view, name="signup_athlete_view"),
    path("signup/as/club/", views.signup_club_view, name="signup_club_view"),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('edit/athlete/<int:user_id>/', views.edit_profile_athlete_view, name='edit_profile_athlete_view'),
    path('edit/club/<int:user_id>/', views.edit_profile_club_view, name='edit_profile_club_view'),

    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='account/Reset_password.html',
        email_template_name='account/password_reset_email.html',
        success_url=reverse_lazy('account:password_reset_done')
    ), name='reset_password'),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password_reset_confirm.html',
        success_url=reverse_lazy('account:password_reset_complete')
    ), name='password_reset_confirm'),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password_reset_complete.html'
    ), name='password_reset_complete'),

    path('add/<int:user_id>', views.add_achievement, name='add_achievement'),
    path('delete/<int:user_id>/<int:pk>/', views.delete_achievement, name='delete_achievement'),



    ]

