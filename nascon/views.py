from django.shortcuts import render
from .models import Event

def index(request):
    # Get all events from the database
    events = Event.objects.all()
    return render(request, "nascon/home.html", {
        "events": events
    })
