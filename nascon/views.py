from typing import Any
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Event, SponsorshipPackage
from .forms import SignupForm, TeamForm
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .models import Event, User, Sponsor, ParticipantEvent, Payment, Team
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm, TeamForm
from functools import wraps


def role_required(role: str): # argument taker
    def require_decorator(view): # decorator
        @wraps(view)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.role != role:
                messages.error(request, f'This page is restricted to {role}')
                # redirect to last page
                return redirect(request.META.get('HTTP_REFERER'))

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
                return redirect(request.POST.get('next') or 'home')
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

        sponsor_obj, created = Sponsor.objects.get_or_create(
            sponsor_id=user,
            event_id=event,
            defaults={'package': package}
        )
        if not created:
            sponsor_obj.package = package
        sponsor_obj.save()
        
        return render(request, 'nascon/sponsor_confirm.html', {
            'package': package,
            'event': event
        })
    
    return redirect('sponsor')

@role_required('participant')
def event_register(request, event_id):
    """First page: Choose solo or team participation"""

    try:
        ParticipantEvent.objects.get(pk=(request.user.id, event_id))
        messages.error(request, 'You are already registered for this event')
        return redirect('events')
    except ParticipantEvent.DoesNotExist:
        try:
            event = Event.objects.get(event_id=event_id)
        except Event.DoesNotExist:
            messages.error(request, "Event not found.")
            return redirect('events')
        
        from datetime import date
        if event.registration_last_date < date.today():
            messages.error(request, "Registration deadline has passed.")
            return redirect('events')
    
        return render(request, 'nascon/event_register.html', { 'event': event })

@role_required('participant')
def team_create(request, event_id):
    """Second page: Create team or register solo"""

    try:
        ParticipantEvent.objects.get(pk=(request.user.id, event_id))
        messages.error(request, 'You are already registered for this event')
        return redirect('events')
    except ParticipantEvent.DoesNotExist:
        try:
            event = Event.objects.get(event_id=event_id)
        except Event.DoesNotExist:
            messages.error(request, "Event not found.")
            return redirect('events')
        
        registration_type = request.GET.get('type', 'solo')
        num_members = 1 if registration_type == 'solo' else event.max_participants
        
        if request.method == 'POST':

            form = TeamForm(num_members, request.POST, initial={ 'event': event_id, 'team_lead': request.user.email })
            if form.is_valid():

                request.session['team_form_data'] = form.cleaned_data
                return redirect('registration_confirm', event_id=event_id)
                
        else:
            form = TeamForm(num_members, initial={ 'event': event_id, 'team_lead': request.user.email })

        query_params = request.GET.urlencode()
        return render(request, 'nascon/team_create.html', { 'form': form, 'event': event, 'query_params': query_params })

@role_required('participant')
def registration_confirm(request, event_id):
    """Third page: Confirm and complete registration"""

    try:
        ParticipantEvent.objects.get(pk=(request.user.id, event_id))
        messages.error(request, 'You are already registered for this event')
        return redirect('events')
    except ParticipantEvent.DoesNotExist:
        try:
            event = Event.objects.get(event_id=event_id)
        except Event.DoesNotExist:
            messages.error(request, "Event not found.")
            return redirect('events')

        cleaned_data: dict[str, Any] = request.session.get('team_form_data', {})

        member_emails = []
        for k,v in cleaned_data.items():
            if k.startswith('member_'):
                member_emails.append(v)

        
        if request.method == 'POST':
            # Create payment with 3-day due date
            from datetime import date, timedelta
            payment = Payment.objects.create(
                amount=event.registration_fees,
                payment_due_date=date.today() + timedelta(days=3)
            )
            
            # Create team
            team = Team.objects.create(
                team_name=cleaned_data['team_name'],
                max_size=event.max_participants,
                score=0,
                event=event,
                paymentid=payment
            )
            # Create participant-event record for team captain
            ParticipantEvent.objects.create(
                participant_id=request.user,
                event_id=event,
                team=team
            )

            for email in member_emails:
                member = User.objects.get(email=email, role='participant')
                ParticipantEvent.objects.create(
                    participant_id=member,
                    event_id=event,
                    team=team
                )
            
            messages.success(request, f"Successfully registered for {event.event_name}!")
            return redirect('events')
        
        return render(request, 'nascon/registration_confirm.html', {
            'event': event,
            'team_name': cleaned_data['team_name'],
            'member_emails': member_emails
        })
