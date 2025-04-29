from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('sponsor/', views.sponsor_view, name="sponsor"),
    path('sponsor/events/', views.sponsor_events_view, name="sponsor_events"),
    path('sponsor/confirm/', views.sponsor_confirm_view, name="sponsor_confirm"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    # path('logout/', views.logout_view, name="logout"),
]
