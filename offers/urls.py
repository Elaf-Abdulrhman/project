from django.urls import path
from . import views

app_name = 'offers'
urlpatterns = [
    path('offer/<int:offer_id>/', views.offer_details, name='offer_details'),
    path('offers/', views.all_offers, name='all_offers'),
    path('add/', views.add_offer, name='add_offer'),
    path('delete/<int:pk>/', views.delete_offer, name='delete_offer'),
    path('edit/<int:pk>/', views.edit_offer, name='edit_offer'),
    path('my_offers/<int:club_id>/', views.my_offers, name='my_offers'),

    path('offer/<int:offer_id>/apply/', views.apply_to_offer, name='apply_to_offer'),
    path('offer/<int:offer_id>/applicants/', views.offer_applicants, name='offer_applicants'),
    path('application/<int:application_id>/respond/', views.respond_to_application, name='respond_to_application'),
    path('my_applications/', views.my_applications, name='my_applications'),


path('application/<int:application_id>/', views.application_detail, name='application_detail'),
path('application/<int:application_id>/response/', views.application_response_detail, name='application_response_detail'),

]

