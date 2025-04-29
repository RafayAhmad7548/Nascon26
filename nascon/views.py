from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Event, SponsorshipPackage
from .forms import SignupForm
from django.contrib.auth import authenticate, login
from .models import Event
from .forms import SignupForm, LoginForm

def index(request):
    # Get all events from the database
    events = Event.objects.all()
    return render(request, "nascon/home.html", {
        "events": events
})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'singup success')
            return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'nascon/signup.html', { 'form' : form })

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'login success')
                return redirect('home')
            else:
                form.add_error('Invalid Credentials', error=ValidationError('Invalid Credentials'))

    else:
        form = LoginForm()
    
    return render(request, 'nascon/login.html', { 'form' : form })

def logout_view(request):
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')



# Add these view functions
def sponsor_view(request):
    """View for the main sponsor page showing available packages"""
    # Dummy data for packages
    packages = SponsorshipPackage.objects.all()
    
    for package in packages:
        # Assuming benefits are stored as text with each benefit on a new line
        if package.benefits:
            package.benefits_list = package.benefits.split(', ')
        else:
            package.benefits_list = []

    return render(request, 'nascon/sponsor.html', {
        'packages': packages
    })

def sponsor_events_view(request):
    """View for selecting which event to sponsor after choosing a package"""
    package_id = request.GET.get('package')
    
    # Get package details based on ID
    packages = {
        '1': {'id': 1, 'name': 'Silver Package', 'price': '5,000'},
        '2': {'id': 2, 'name': 'Gold Package', 'price': '10,000'},
        '3': {'id': 3, 'name': 'Platinum Package', 'price': '500,000'}
    }
    
    package = packages.get(package_id)
    
    # Get events from database or use dummy data
    events = Event.objects.all()
    
    # # If no events in database, use dummy events
    # if not events:
    #     events = [
    #         {
    #             'event_id': 1,
    #             'event_name': 'Coding Competition',
    #             'description': 'A competitive programming contest for university students',
    #             'category': 'Technical',
    #             'date_time': '2026-02-15 10:00:00'
    #         },
    #         {
    #             'event_id': 2,
    #             'event_name': 'Business Case Competition',
    #             'description': 'Present innovative solutions to real-world business problems',
    #             'category': 'Business',
    #             'date_time': '2026-02-16 11:00:00'
    #         },
    #         {
    #             'event_id': 3,
    #             'event_name': 'Gaming Tournament',
    #             'description': 'Compete in various gaming categories from esports to board games',
    #             'category': 'Gaming',
    #             'date_time': '2026-02-17 09:00:00'
    #         }
    #     ]
    
    return render(request, 'nascon/sponsor_events.html', {
        'package': package,
        'events': events
    })

def sponsor_confirm_view(request):
    """Handle form submission and show confirmation"""
    if request.method == 'POST':
        package_id = request.POST.get('package_id')
        event_id = request.POST.get('event_id')
        
        # Get package details
        packages = {
            '1': {'id': 1, 'name': 'Silver Package', 'price': '100,000'},
            '2': {'id': 2, 'name': 'Gold Package', 'price': '250,000'},
            '3': {'id': 3, 'name': 'Platinum Package', 'price': '500,000'}
        }
        
        package = packages.get(package_id)
        
        # Get event details - try database first, then fall back to dummy data
        try:
            event = Event.objects.get(event_id=event_id)
        except:
            # Dummy events
            events = {
                '1': {'event_id': 1, 'event_name': 'Coding Competition', 'date_time': '2026-02-15 10:00:00'},
                '2': {'event_id': 2, 'event_name': 'Business Case Competition', 'date_time': '2026-02-16 11:00:00'},
                '3': {'event_id': 3, 'event_name': 'Gaming Tournament', 'date_time': '2026-02-17 09:00:00'}
            }
            event = events.get(event_id)
        
        return render(request, 'nascon/sponsor_confirm.html', {
            'package': package,
            'event': event
        })
    
    return redirect('sponsor')
