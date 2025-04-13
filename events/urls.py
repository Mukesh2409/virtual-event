from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # Event listing and details
    path('', views.event_list, name='event_list'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    
    # Event management
    path('create/', views.event_create, name='event_create'),
    path('<int:event_id>/edit/', views.event_edit, name='event_edit'),
    path('<int:event_id>/delete/', views.event_delete, name='event_delete'),
    path('my-events/', views.my_events, name='my_events'),
    path('<int:event_id>/manage/', views.event_manage, name='event_manage'),
    
    # Event registration
    path('<int:event_id>/register/', views.event_register, name='event_register'),
    path('<int:event_id>/unregister/', views.event_unregister, name='event_unregister'),
    
    # Sessions
    path('<int:event_id>/sessions/add/', views.add_session, name='add_session'),
    path('<int:event_id>/sessions/<int:session_id>/delete/', views.delete_session, name='delete_session'),
    
    # Livestream and chat
    path('<int:event_id>/livestream/', views.livestream, name='livestream'),
    path('<int:event_id>/chat/send/', views.send_chat, name='send_chat'),
    path('<int:event_id>/chat/messages/', views.get_chat_messages, name='get_chat_messages'),
]