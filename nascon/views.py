# from django.shortcuts import render
# from .models import Event

# def index(request):
#     # Get all events from the database
#     events = Event.objects.all()
#     return render(request, "nascon/home.html", {
#         "events": events
#     })
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .models import Event, User
from .forms import SignupForm, LoginForm
# import bcrypt
import random

def index(request):
    # Get all events from the database
    events = Event.objects.all()
    return render(request, "nascon/home.html", {
        "events": events
    })

def signup_view(request):
    # if request.method == 'POST':
    #     form = SignupForm(request.POST)
    #     if form.is_valid():
    #         try:
    #             with transaction.atomic():
    #                 # Generate hash for password
    #                 password = form.cleaned_data['password']
    #                 hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    #
    #                 # Find max user ID and add 1 for new user
    #                 max_userid = User.objects.all().order_by('-userid').first()
    #                 new_userid = 1
    #                 if max_userid:
    #                     new_userid = max_userid.userid + 1
    #
    #                 # Create new user
    #                 user = User(
    #                     userid=new_userid,
    #                     username=form.cleaned_data['username'],
    #                     email=form.cleaned_data['email'],
    #                     password=hashed_password.decode(),  # Store hashed password as string
    #                     role=form.cleaned_data['role']
    #                 )
    #                 user.save()
    #
    #                 # Set session data
    #                 request.session['user_id'] = user.userid
    #                 request.session['username'] = user.username
    #                 request.session['role'] = user.role
    #
    #                 messages.success(request, 'Account created successfully!')
    #                 return redirect('home')
    #         except Exception as e:
    #             messages.error(request, f'An error occurred: {str(e)}')
    # else:
    #     form = SignupForm()
    
    return render(request, 'nascon/signup.html')

def login_view(request):
    # if request.method == 'POST':
    #     form = LoginForm(request.POST)
    #     if form.is_valid():
    #         username_or_email = form.cleaned_data['username_or_email']
    #         password = form.cleaned_data['password']
    #
    #         # Check if user exists by username or email
    #         try:
    #             # Try to find by username
    #             user = User.objects.filter(username=username_or_email).first()
    #             if not user:
    #                 # Try to find by email
    #                 user = User.objects.filter(email=username_or_email).first()
    #
    #             if user and bcrypt.checkpw(password.encode(), user.password.encode()):
    #                 # Authentication successful
    #                 request.session['user_id'] = user.userid
    #                 request.session['username'] = user.username
    #                 request.session['role'] = user.role
    #                 messages.success(request, 'Login successful!')
    #                 return redirect('home')
    #             else:
    #                 messages.error(request, 'Invalid username/email or password.')
    #         except Exception as e:
    #             messages.error(request, f'An error occurred: {str(e)}')
    # else:
    #     form = LoginForm()
    
    return render(request, 'nascon/login.html')

def logout_view(request):
    # Clear all session data
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

# Add these view functions
def sponsor_view(request):
    """View for the main sponsor page showing available packages"""
    # Dummy data for packages
    packages = [
        {
            'id': 1,
            'name': 'Silver Package',
            'price': '100,000',
            'benefits': [
                'Logo on event website',
                'Social media mentions',
                'Booth at the venue'
            ]
        },
        {
            'id': 2,
            'name': 'Gold Package',
            'price': '250,000',
            'benefits': [
                'All Silver benefits',
                'Larger booth space',
                'Logo on event shirts',
                'Speaking opportunity'
            ]
        },
        {
            'id': 3,
            'name': 'Platinum Package',
            'price': '500,000',
            'benefits': [
                'All Gold benefits',
                'Named event sponsorship',
                'Premium booth location',
                'Access to participant resumes'
            ]
        }
    ]
    
    return render(request, 'nascon/sponsor.html', {
        'packages': packages
    })

def sponsor_events_view(request):
    """View for selecting which event to sponsor after choosing a package"""
    package_id = request.GET.get('package')
    
    # Get package details based on ID
    packages = {
        '1': {'id': 1, 'name': 'Silver Package', 'price': '100,000'},
        '2': {'id': 2, 'name': 'Gold Package', 'price': '250,000'},
        '3': {'id': 3, 'name': 'Platinum Package', 'price': '500,000'}
    }
    
    package = packages.get(package_id)
    
    # Get events from database or use dummy data
    events = Event.objects.all()
    
    # If no events in database, use dummy events
    if not events:
        events = [
            {
                'event_id': 1,
                'event_name': 'Coding Competition',
                'description': 'A competitive programming contest for university students',
                'category': 'Technical',
                'date_time': '2026-02-15 10:00:00'
            },
            {
                'event_id': 2,
                'event_name': 'Business Case Competition',
                'description': 'Present innovative solutions to real-world business problems',
                'category': 'Business',
                'date_time': '2026-02-16 11:00:00'
            },
            {
                'event_id': 3,
                'event_name': 'Gaming Tournament',
                'description': 'Compete in various gaming categories from esports to board games',
                'category': 'Gaming',
                'date_time': '2026-02-17 09:00:00'
            }
        ]
    
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