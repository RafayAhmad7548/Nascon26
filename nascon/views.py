from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Event, SponsorshipPackage
from .forms import SignupForm
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .models import Event, User, Sponsor, ParticipantEvent, Payment, Team
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
        selected_role = request.GET.get('role', '')
        form = SignupForm(initial={'role': selected_role})
    

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
                messages.success(request, 'Login Successful')
                next = request.POST.get('next')
                if next:
                    return redirect(next)
                return redirect('home')
            else:
                form.add_error('password', error=ValidationError('Invalid Credentials'))



    else:
        form = LoginForm()
    
    return render(request, 'nascon/login.html', { 'form' : form })

def logout_view(request):
    request.session.flush()
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def events_view(request):
    filter = request.GET.get('filter')
    if filter is None:
        events = Event.objects.all().order_by('date_time')
    else:
        events = Event.objects.filter(category__exact=filter)
    return render(request, 'nascon/events.html', { 'events': events })


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

        package = SponsorshipPackage.objects.get(package_id=package_id)
        event = Event.objects.get(event_id=event_id)

        # Insert into Sponsor table (avoid duplicates in keys)
        sponsor_obj, created = Sponsor.objects.get_or_create(
            sponsor_id=user,
            event_id=event,
            defaults={'package': package}
        )
        if not created:
            sponsor_obj.package = package  # Update package if already exists
        sponsor_obj.save()
        
        return render(request, 'nascon/sponsor_confirm.html', {
            'package': package,
            'event': event
        })
    
    return redirect('sponsor')

@login_required
def event_register(request, event_id):
    """First page: Choose solo or team participation"""
    # Get event details
    try:
        event = Event.objects.get(event_id=event_id)
    except Event.DoesNotExist:
        messages.error(request, "Event not found.")
        return redirect('events')
    
    # Check user role is participant
    if request.user.role != 'participant':
        messages.error(request, "Only participants can register for events.")
        return redirect('events')
    
    # Check registration deadline
    from datetime import date
    if event.registration_last_date < date.today():
        messages.error(request, "Registration deadline has passed.")
        return redirect('events')
    
    return render(request, 'nascon/event_register.html', {'event': event})

@login_required
def team_create(request, event_id):
    """Second page: Create team or register solo"""
    try:
        event = Event.objects.get(event_id=event_id)
    except Event.DoesNotExist:
        messages.error(request, "Event not found.")
        return redirect('events')
    
    # Get registration type
    registration_type = request.GET.get('type', 'solo')
    is_team = registration_type == 'team'
    
    if request.method == 'POST':
        # Process form submission
        team_name = request.POST.get('team_name')
        member_emails = request.POST.getlist('member_email')
        
        # Store in session for confirmation page
        request.session['registration_data'] = {
            'event_id': event_id,
            'team_name': team_name,
            'member_emails': member_emails,
            'is_team': is_team
        }
        
        return redirect('registration_confirm', event_id=event_id)
    
    return render(request, 'nascon/team_create.html', {
        'event': event,
        'is_team': is_team
    })

@login_required
def registration_confirm(request, event_id):
    """Third page: Confirm and complete registration"""
    # Get data from session
    registration_data = request.session.get('registration_data', {})
    
    try:
        event = Event.objects.get(event_id=event_id)
    except Event.DoesNotExist:
        messages.error(request, "Event not found.")
        return redirect('events')
    
    if request.method == 'POST':
        # Create payment with 3-day due date
        from datetime import date, timedelta
        payment = Payment.objects.create(
            amount=event.registration_fees,
            payment_due_date=date.today() + timedelta(days=3)
        )
        
        # Create team
        team = Team.objects.create(
            team_name=registration_data['team_name'],
            max_size=event.max_participants,
            score=0,
            paymentid=payment
        )
        # Create participant-event record for team captain
        ParticipantEvent.objects.create(
            participant_id=request.user,
            event_id=event,
            team=team
        )
        # Create participant-event records for team members
        if registration_data.get('is_team'):
            for email in registration_data.get('member_emails', []):
                if email:
                    try:
                        member = User.objects.get(email=email, role='participant')
                        ParticipantEvent.objects.create(
                            participant_id=member,
                            event_id=event,
                            team=team
                        )
                    except User.DoesNotExist:
                        pass
        
        messages.success(request, f"Successfully registered for {event.event_name}!")
        return redirect('events')
    
    return render(request, 'nascon/registration_confirm.html', {
        'event': event,
        'registration_data': registration_data
    })

def check_team_name(request):
    """Validate if team name is unique"""
    team_name = request.GET.get('name', '')
    exists = Team.objects.filter(team_name=team_name).exists()
    return JsonResponse({'exists': exists})

def check_member_email(request):
    """Validate if email belongs to a participant"""
    email = request.GET.get('email', '')
    try:
        user = User.objects.get(email=email)
        return JsonResponse({
            'exists': True,
            'is_participant': user.role == 'participant'
        })
    except User.DoesNotExist:
        return JsonResponse({
            'exists': False,
            'is_participant': False
        })
    
