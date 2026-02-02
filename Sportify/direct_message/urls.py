from django.urls import path
from . import views

app_name = 'direct_message'

urlpatterns = [
    path('', views.chat_page_view, name='chat_page_view'),
    path('<str:username>/', views.chat_page_view, name='chat_page'),
    path('edit/<int:message_id>/', views.edit_message_view, name='edit_message'),
    path('message/delete_for_me/<int:message_id>/', views.delete_message_for_me, name='delete_message_for_me'),
    path('message/delete_for_everyone/<int:message_id>/', views.delete_message_for_everyone, name='delete_message_for_everyone'),
    path('conversation/clear/<str:username>/', views.clear_conversation, name='clear_conversation'),
]
