from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('events/', views.events_view, name='events'),
    path('sponsor/', views.sponsor_view, name="sponsor"),
    path('sponsor/events/', views.sponsor_events_view, name="sponsor_events"),
    path('sponsor/confirm/', views.sponsor_confirm_view, name="sponsor_confirm"),
    path('login/', views.login_view, name="login"),
    path('signup/', views.signup_view, name="signup"),
    path('logout/', views.logout_view, name="logout"),
    path('events/register/<int:event_id>/', views.event_register, name='event_register'),
    path('events/register/<int:event_id>/team/', views.team_create, name='team_create'),
    path('events/register/<int:event_id>/confirm/', views.registration_confirm, name='registration_confirm'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('events/<int:event_id>/participants/', views.event_participants_view, name='event_participants'),
    path('events/organize', views.orgainze_event, name='organize_event'),
]
