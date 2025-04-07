from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_events, name='event-list'),
    path('create/', views.create_event, name='event-create'),
    path('<int:event_id>/', views.get_event, name='event-detail'),
    path('<int:event_id>/update/', views.update_event, name='event-update'),
    path('<int:event_id>/delete/', views.delete_event, name='event-delete'),
    path('<int:event_id>/register/', views.register_for_event, name='event-register'),
    path('registrations/my-events/', views.get_registered_events, name='user-registered-events')
]