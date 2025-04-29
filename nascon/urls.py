from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('login/', views.login_view, name="login"),
    path('signup/', views.signup_view, name="signup"),
    path('logout/', views.logout_view, name="logout"),
    path('sponsor/', views.sponsor_view, name="sponsor"),
    path('sponsor/events/', views.sponsor_events_view, name="sponsor_events"),
    path('sponsor/confirm/', views.sponsor_confirm_view, name="sponsor_confirm"),
]
