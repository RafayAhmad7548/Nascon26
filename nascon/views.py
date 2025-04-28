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
