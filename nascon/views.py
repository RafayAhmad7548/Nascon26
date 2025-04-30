from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Event, SponsorshipPackage
from .forms import SignupForm
from django.contrib.auth import authenticate, login, logout
from .models import Event, User, Sponsor
from .forms import SignupForm, LoginForm
from functools import wraps

def sponsor_required(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            messages.error(request, "Please log in to access the sponsor area.")
            return redirect('login')
        
        # Check if user has sponsor role
        if request.user.role != 'sponsor':
            messages.error(request, "This area is restricted to sponsors only.")
            return redirect('home')
            
        return function(request, *args, **kwargs)
    return wrapper

def index(request):
    # Get all events from the database
    events = Event.objects.all()
    return render(request, "nascon/home.html", {
        "events": events
})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registered Successfully')
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
            
            try:
                User.objects.get(email=email)

                user = authenticate(request, username=email, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Login Successful')
                    return redirect('home')
                else:
                    form.add_error('password', error=ValidationError('Invalid Credentials'))

            except User.DoesNotExist:
                form.add_error('email', error=ValidationError('Email not registered'))


    else:
        form = LoginForm()
    
    return render(request, 'nascon/login.html', { 'form' : form })

def logout_view(request):
    request.session.flush()
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')



# Add these view functions
@sponsor_required
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

@sponsor_required
def sponsor_events_view(request):
    """View for selecting which event to sponsor after choosing a package"""
    package_id = request.GET.get('package')
    
    package = SponsorshipPackage.objects.get(package_id__exact=package_id)
    
    # Get events from database or use dummy data
    events = Event.objects.all()
    
    return render(request, 'nascon/sponsor_events.html', {
        'package': package,
        'events': events
    })

def events_view(request):
    events = Event.objects.all().order_by('date_time')
    return render(request, 'nascon/events.html', {'events': events})

@sponsor_required
def sponsor_confirm_view(request):
    """Handle form submission and show confirmation"""
    if request.method == 'POST':
        package_id = request.POST.get('package_id')
        event_id = request.POST.get('event_id')
        user = request.user

        # Fetch related objects
        package = SponsorshipPackage.objects.get(package_id=package_id)
        event = Event.objects.get(event_id=event_id)

        # Insert into Sponsor table
        sponsor_obj = Sponsor.objects.create(
            sponsor_id=user,
            event_id=event,
            package_id=package_id
        )
        sponsor_obj.save()
        
        return render(request, 'nascon/sponsor_confirm.html', {
            'package': package,
            'event': event
        })
    
    return redirect('sponsor')
