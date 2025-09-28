from django.urls import path
from . import views

app_name = 'calendar_app'

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('event/<int:event_id>/', views.event_detail_view, name='event_detail'),
    path('create-event/', views.create_event_view, name='create_event'),
    path('api/events/', views.events_api, name='events_api'),
]