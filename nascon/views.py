from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Event, SponsorshipPackage
from .forms import SignupForm
from django.contrib.auth import authenticate, login, logout
from .models import Event, User, Sponsor
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm
from functools import wraps


def role_required(role: str): # argument taker
    def require_decorator(view): # decorator
        @wraps(view)
        @login_required
        def wrapper(request, *args, **kwargs):
            print('wrapper called')
            if request.user.role != role:
                messages.error(request, f'This page is restricted to {role}')
                return redirect('home')

            return view(request, *args, **kwargs)

        return wrapper
    return require_decorator


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
                    next = request.POST.get('next')
                    if next:
                        return redirect(next)
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


def events_view(request):
    events = Event.objects.all().order_by('date_time')
    return render(request, 'nascon/events.html', {'events': events})


@role_required('sponsor')
def sponsor_view(request):
    """View for the main sponsor page showing available packages"""
    # Dummy data for packages
    packages = SponsorshipPackage.objects.all()
    
    benefits_list = []
    for package in packages:
        if package.benefits:
            benefits_list = package.benefits.split(', ')

    return render(request, 'nascon/sponsor.html', {
        'packages': packages,
        'benefits': benefits_list
    })

@role_required('sponsor')
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

@role_required('sponsor')
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
