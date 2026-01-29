# NaSCon 2026 - National Student Convention Management System

[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-Database-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-Educational-yellow.svg)]()

A comprehensive web-based event management system designed to streamline the organization, registration, and management of a national student convention. The platform supports multiple user roles including participants, organizers, judges, sponsors, and societies with role-based access control and tailored dashboards for each user type.

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Database Architecture](#database-architecture)
- [Installation & Setup](#installation--setup)
- [Project Structure](#project-structure)
- [User Roles & Permissions](#user-roles--permissions)
- [Core Functionalities](#core-functionalities)
- [Implementation Details](#implementation-details)
- [Security Features](#security-features)
- [Screenshots](#screenshots)
- [Contributors](#contributors)

## 🎯 Project Overview

NaSCon 2026 is a full-stack web application built with Django that manages all aspects of a national student convention. The system handles event creation, participant registration, team formation, sponsorship management, venue allocation, payment processing, and role-based access control. It provides a centralized platform for coordinating complex multi-stakeholder event operations.

**Academic Context:** Database Systems Project - Semester 04  
**Development Period:** 2025-2026

## ✨ Features

### For Participants
- **User Registration & Authentication** - Email-based authentication with secure password hashing
- **Event Discovery** - Browse events with category-based filtering (Technical, Business, Gaming, General)
- **Team Registration** - Create teams or register as solo participants
- **Multi-step Registration Process** - Choose participation type → Create/Join team → Confirm registration
- **Team Management** - Dynamic team creation with validation for duplicate members and registration status
- **Personalized Dashboard** - View registered events, team details, event rounds, and payment status
- **Registration Deadlines** - Automatic validation against event registration closing dates
- **Payment Tracking** - View payment due dates and amounts

### For Organizers
- **Event Creation** - Comprehensive event setup with detailed validation
  - Event name, description, and categorization
  - Maximum participant limits (1-12 per team)
  - Registration fees (₹500-₹5000, divisible by 10)
  - Registration deadlines (minimum 3 days in advance)
  - Event date/time (minimum 3 days after registration deadline)
  - Judge assignment via email lookup
- **Participant Management** - View all registered teams and participants for each event
- **Event Monitoring** - Track participant count, team count, and event rounds
- **Dashboard Analytics** - Overview of all organized events with statistics

### For Sponsors
- **Sponsorship Packages** - Browse available sponsorship tiers with benefits
- **Event Selection** - Choose which events to sponsor
- **Multi-step Sponsorship** - Select package → Choose event → Confirm sponsorship
- **Sponsorship Dashboard** - View all sponsored events and package details
- **Benefits Display** - Detailed breakdown of sponsorship benefits

### For Judges
- **Event Assignment** - View all events assigned for judging
- **Event Round Details** - Access complete round information including venues and timings
- **Dashboard** - Centralized view of all judging responsibilities

### General Features
- **Role-Based Access Control (RBAC)** - Custom decorators for route protection
- **Responsive Design** - Mobile-friendly interface using CSS
- **Flash Messages** - User feedback for all operations (success, error, warnings)
- **Session Management** - Secure session handling for multi-step processes
- **Dynamic Form Generation** - Forms adapt based on event requirements and user inputs
- **Validation** - Comprehensive server-side validation for all user inputs

## 🛠 Technology Stack

### Backend Framework
- **Django 5.2** - High-level Python web framework
  - MTV (Model-Template-View) architecture
  - Built-in admin panel
  - ORM (Object-Relational Mapping)
  - Middleware support
  - URL routing system

### Database
- **MySQL** - Relational database management system
  - Remote database hosting (alra.ddns.net:3306)
  - MySQLdb/mysqlclient 2.2.7 - Python MySQL connector
  - UTF-8 character encoding support
  - Configuration via `mysql.cnf`

### Authentication & Security
- **Django Authentication System** - Built-in authentication backend
  - Custom user model extending `AbstractUser`
  - Email-based authentication (instead of username)
  - bcrypt 4.3.0 - Password hashing algorithm
  - CSRF protection middleware
  - Session-based authentication
  - Password validation with multiple validators

### Frontend
- **Django Templates** - Server-side template rendering
  - Template inheritance (base.html)
  - Template tags and filters
  - Static file management
- **HTML5/CSS3** - Modern web standards
  - Custom CSS components (header, footer, forms)
  - Responsive design
- **JavaScript** - Client-side interactivity
- **Font Awesome 6.0** - Icon library for UI elements

### Additional Libraries
- **asgiref 3.8.1** - ASGI (Asynchronous Server Gateway Interface) support
- **sqlparse 0.5.3** - SQL parsing and formatting
- **tzdata 2025.2** - Timezone data

### Development Tools
- **Python Virtual Environment (venv)** - Dependency isolation
- **pip 24.0** - Package management
- **PowerShell** - Terminal environment (Windows)

## 🗄 Database Architecture

### Entity-Relationship Model

The database follows a normalized relational design with the following key entities:

#### Core Entities

**1. User (Custom Authentication)**
- Extends Django's `AbstractUser`
- Email as unique identifier (USERNAME_FIELD)
- Role-based differentiation (participant, organizer, judge, society, sponsor)
- Foreign key to Accommodation
```python
Fields: id, email*, username, first_name, last_name, password, role, accommodation_id
Unique: email
Authentication: email + password
```

**2. Event**
- Central entity for convention activities
- Categorized events (technical, business, gaming, general)
- Links to organizer and judge users
- Comprehensive event details
```python
Fields: event_id (PK), event_name*, description, category, max_participants, 
        registration_fees, registration_last_date, date_time, 
        organizer_id (FK→User), judge_id (FK→User)
Unique: event_name
Constraints: max_participants (1-12), fees (500-5000, ÷10)
```

**3. Team**
- Composite teams for events
- Linked to payment records
- Score tracking capability
```python
Fields: team_id (PK), team_name, max_size, score, event (FK→Event), 
        paymentid (FK→Payment)
Unique: (team_name, event)
```

**4. ParticipantEvent (Junction Table)**
- Many-to-many relationship between Users and Events
- Composite primary key
- Team assignment
```python
Fields: participant_id (FK→User), event_id (FK→Event), team (FK→Team)
Primary Key: (participant_id, event_id)
Unique: (participant_id, event_id)
```

**5. Sponsor (Junction Table)**
- Links sponsors to events with packages
- Composite primary key
```python
Fields: sponsor_id (FK→User), event_id (FK→Event), package (FK→SponsorshipPackage)
Primary Key: (sponsor_id, event_id)
Unique: (sponsor_id, event_id)
```

**6. EventRound**
- Multiple rounds per event
- Venue and timing management
- Composite primary key
```python
Fields: round_id, event_id (FK→Event), round_type, start_time, venue_id (FK→Venue)
Primary Key: (round_id, event_id)
Unique: (round_id, event_id), (start_time, venue_id)
```

**7. Venue**
```python
Fields: venue_id (PK), venue_name, capacity, location
```

**8. Payment**
```python
Fields: payment_id (PK), amount, payment_due_date
Auto-calculated: due_date = registration_date + 3 days
```

**9. SponsorshipPackage**
```python
Fields: package_id (PK), category, benefits (comma-separated), cost
```

**10. Society**
```python
Fields: society_id (PK), user_id (FK→User), society_name*, description
Unique: society_name
```

**11. Accommodation**
```python
Fields: accommodation_id (PK), room_number, checkin_date, checkout_date, cost
```

### Database Relationships

- **User → Event**: One-to-Many (organizer)
- **User → Event**: One-to-Many (judge)
- **User ↔ Event**: Many-to-Many (participants via ParticipantEvent)
- **User ↔ Event**: Many-to-Many (sponsors via Sponsor)
- **Event → Team**: One-to-Many
- **Event → EventRound**: One-to-Many
- **Venue → EventRound**: One-to-Many
- **Team → ParticipantEvent**: One-to-Many
- **Payment → Team**: One-to-One
- **SponsorshipPackage → Sponsor**: One-to-Many
- **Accommodation → User**: One-to-Many

### Key Constraints & Validations

1. **Unique Constraints**: Email, event_name, society_name, (team_name, event)
2. **Composite Primary Keys**: ParticipantEvent, Sponsor, EventRound
3. **Date Validations**: registration_last_date ≥ today + 3 days, event_date ≥ reg_last_date + 3 days
4. **Numeric Constraints**: max_participants (1-12), fees (500-5000, divisible by 10)
5. **Foreign Key Cascades**: CASCADE for critical relationships, DO_NOTHING for historical data

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- MySQL Server (local or remote access)
- pip (Python package manager)
- Git (optional, for version control)

### Step-by-Step Installation

#### 1. Clone or Download the Project
```powershell
# If using Git
git clone <repository-url>
cd Nascon26

# Or download and extract ZIP, then navigate to the folder
cd F:\Semester_04\DB\Project\Nascon26
```

#### 2. Create Virtual Environment
```powershell
# Create virtual environment
python -m venv env

# Activate virtual environment (PowerShell)
.\env\Scripts\Activate.ps1

# For Command Prompt
.\env\Scripts\activate.bat

# For Linux/Mac
source env/bin/activate
```

#### 3. Install Dependencies
```powershell
# Install all required packages
pip install django==5.2
pip install mysqlclient==2.2.7
pip install bcrypt==4.3.0

# Or if requirements.txt exists
pip install -r requirements.txt
```

#### 4. Configure Database

**Edit `mysql.cnf`** with your database credentials:
```ini
[client]
database = your_database_name
user = your_mysql_username
password = your_mysql_password
host = localhost  # or remote host
port = 3306
default-character-set = utf8mb4
```

**Create MySQL Database:**
```sql
CREATE DATABASE your_database_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 5. Configure Django Settings

**Edit `Nascon26/settings.py`**:
- Update `SECRET_KEY` for production
- Set `DEBUG = False` for production
- Add your domain to `ALLOWED_HOSTS`
```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'yourdomain.com']
```

#### 6. Apply Database Migrations
```powershell
# Create migration files (if modified models)
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Verify migration status
python manage.py showmigrations
```

#### 7. Create Superuser (Admin)
```powershell
python manage.py createsuperuser
# Follow prompts to enter email, username, and password
```

#### 8. Collect Static Files (Production)
```powershell
python manage.py collectstatic
```

#### 9. Run Development Server
```powershell
python manage.py runserver

# Access at: http://127.0.0.1:8000/
# Admin panel: http://127.0.0.1:8000/admin/
```

#### 10. Initial Data Setup (Optional)

Access admin panel and create:
- Sample users (participants, organizers, judges, sponsors)
- Sponsorship packages
- Venues
- Events

### Troubleshooting

**MySQL Connection Issues:**
```powershell
# Verify MySQL is running
mysql --version

# Test connection
mysql -h host -u user -p database_name
```

**Migration Errors:**
```powershell
# Reset migrations (WARNING: deletes data)
python manage.py migrate --fake nascon zero
python manage.py migrate nascon
```

**Virtual Environment Issues:**
```powershell
# If activation fails on Windows
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📁 Project Structure

```
Nascon26/
│
├── manage.py                      # Django management script
├── mysql.cnf                      # MySQL database configuration
├── README.md                      # This file
│
├── env/                           # Virtual environment (not in version control)
│   ├── Lib/site-packages/        # Installed Python packages
│   ├── Scripts/                   # Activation scripts
│   └── pyvenv.cfg                # Environment configuration
│
├── Nascon26/                      # Project configuration package
│   ├── __init__.py               # Python package marker
│   ├── settings.py               # Django settings (database, installed apps, middleware)
│   ├── urls.py                   # Root URL configuration
│   ├── asgi.py                   # ASGI application entry point
│   ├── wsgi.py                   # WSGI application entry point
│   └── __pycache__/              # Python bytecode cache
│
└── nascon/                        # Main application package
    │
    ├── __init__.py               # Python package marker
    ├── admin.py                  # Django admin configuration
    ├── apps.py                   # Application configuration
    ├── models.py                 # Database models (11 models)
    ├── views.py                  # View functions (14 views)
    ├── urls.py                   # Application URL patterns
    ├── forms.py                  # Django forms (4 forms)
    ├── tests.py                  # Unit tests
    │
    ├── migrations/               # Database migrations
    │   ├── __init__.py
    │   ├── 0001_initial.py       # Initial database schema
    │   ├── 0002_alter_user_role.py
    │   ├── 0003_alter_event_category.py
    │   ├── 0004_team_event_alter_team_team_name_and_more.py
    │   ├── 0005_alter_event_event_name_and_more.py
    │   └── __pycache__/
    │
    ├── static/nascon/            # Static files (CSS, JS, Images)
    │   ├── css/
    │   │   ├── main.css          # Core styles
    │   │   └── components/       # Component-specific styles
    │   │       ├── header.css
    │   │       └── footer.css
    │   ├── js/                   # JavaScript files
    │   └── images/               # Image assets
    │       └── logo.png          # Application logo
    │
    ├── templates/                # HTML templates
    │   ├── base.html             # Base template with navigation
    │   └── nascon/               # Application templates
    │       ├── home.html                     # Landing page
    │       ├── events.html                   # Event listing
    │       ├── signup.html                   # User registration
    │       ├── login.html                    # User login
    │       ├── dashboard.html                # Role-based dashboard
    │       ├── event_register.html           # Step 1: Registration type
    │       ├── team_create.html              # Step 2: Team creation
    │       ├── registration_confirm.html     # Step 3: Confirmation
    │       ├── organize_event.html           # Event creation (organizer)
    │       ├── event_participants.html       # Participant list (organizer)
    │       ├── sponsor.html                  # Sponsorship packages
    │       ├── sponsor_events.html           # Event selection (sponsor)
    │       └── sponsor_confirm.html          # Sponsorship confirmation
    │
    └── __pycache__/              # Python bytecode cache
```

### Key Files Explained

**Configuration Files:**
- `settings.py`: Database connection, installed apps, middleware, authentication backend
- `mysql.cnf`: MySQL connection parameters
- `urls.py`: URL routing to views

**Application Logic:**
- `models.py`: 11 database models with relationships and validations
- `views.py`: 14 view functions handling business logic
- `forms.py`: 4 Django forms with custom validation (SignupForm, LoginForm, TeamForm, EventForm)

**Templates:**
- `base.html`: Master template with header, navigation, flash messages
- Page-specific templates extending base template

## 👥 User Roles & Permissions

### 1. Participant
**Registration:** Self-registration with email verification  
**Permissions:**
- ✅ Browse all events
- ✅ Register for events (solo or team)
- ✅ Create teams and invite members
- ✅ View personal dashboard with registered events
- ✅ View team details and payment status
- ❌ Create events
- ❌ View other participants' details
- ❌ Access admin panel

**Dashboard View:** Events registered, team information, event rounds, payment dues

### 2. Organizer
**Registration:** Self-registration (role selection during signup)  
**Permissions:**
- ✅ Create new events
- ✅ Assign judges to events
- ✅ View participants for their events
- ✅ View team compositions
- ✅ Monitor registration statistics
- ❌ Register as participant
- ❌ Modify other organizers' events

**Dashboard View:** Organized events, participant count, team count, event rounds

### 3. Judge
**Registration:** Self-registration (role selection during signup)  
**Assignment:** By organizers during event creation  
**Permissions:**
- ✅ View assigned events
- ✅ View event rounds and schedules
- ✅ View venue information
- ❌ Create or modify events
- ❌ View participant details

**Dashboard View:** Assigned events, round details, venue information

### 4. Sponsor
**Registration:** Self-registration (role selection during signup)  
**Permissions:**
- ✅ Browse sponsorship packages
- ✅ Select events to sponsor
- ✅ View sponsored events
- ✅ View package benefits
- ❌ Create events
- ❌ View financial details of events

**Dashboard View:** Sponsored events, package details, benefits breakdown

### 5. Society
**Registration:** Self-registration (role selection during signup)  
**Status:** Model exists but not yet implemented in views  
**Future Scope:** Society management and event organization

### Access Control Implementation

**Custom Decorator:**
```python
@role_required('participant')
def participant_only_view(request):
    # Only accessible to participants
```

**Middleware Protection:**
- `django.contrib.auth.middleware.AuthenticationMiddleware`
- `@login_required` decorator for authenticated-only routes

**URL Protection:**
- Login URL: `/login/`
- Redirect to `HTTP_REFERER` on unauthorized access
- Flash messages for permission errors

## 🔧 Core Functionalities

### 1. Authentication System

#### User Registration
- **Route:** `/signup/`
- **Features:**
  - Role selection (participant, organizer, judge, sponsor, society)
  - Email uniqueness validation
  - Password confirmation matching
  - Bcrypt password hashing
  - Custom user model with email as USERNAME_FIELD
- **Form:** `SignupForm` (ModelForm)
- **Validation:**
  - Required: first_name, last_name, username, email, password
  - Custom: Password matching validation
  - Model: Email uniqueness constraint

#### User Login
- **Route:** `/login/`
- **Features:**
  - Email-based authentication
  - Session creation
  - Next URL redirection
  - Invalid credential handling
- **Form:** `LoginForm` (Form)
- **Validation:**
  - Email existence check
  - Password verification via `authenticate()`

#### Logout
- **Route:** `/logout/`
- **Features:**
  - Session flush
  - Complete logout
  - Redirect to home

### 2. Event Management

#### Event Creation (Organizers Only)
- **Route:** `/events/organize`
- **Decorator:** `@role_required('organizer')`
- **Form Fields:**
  - Event name (unique)
  - Description
  - Category (technical/business/gaming/general)
  - Max participants per team (1-12)
  - Registration fees (₹500-5000, divisible by 10)
  - Registration last date (≥ today + 3 days)
  - Event date/time (≥ reg_last_date + 3 days)
  - Judge email (must exist with 'judge' role)
- **Validations:**
  - Custom clean methods for each field
  - Cross-field validation for dates
  - Judge existence verification
- **Auto-assignment:** Current user set as organizer

#### Event Listing
- **Route:** `/events/`
- **Features:**
  - Display all events ordered by date
  - Category-based filtering via query parameter
  - Event cards with details
- **Query:** `Event.objects.all().order_by('date_time')`

#### Event Details
- **View:** Participants can view event information before registration
- **Data:** Name, description, category, fees, dates, max participants

### 3. Participant Registration (Multi-Step Process)

#### Step 1: Choose Registration Type
- **Route:** `/events/register/<event_id>/`
- **Decorator:** `@role_required('participant')`
- **Validations:**
  - User not already registered for event
  - Event exists
  - Registration deadline not passed
- **Options:**
  - Solo registration
  - Team registration

#### Step 2: Team Creation
- **Route:** `/events/register/<event_id>/team/?type=solo|team`
- **Decorator:** `@role_required('participant')`
- **Dynamic Form:**
  - Team name input
  - Team lead (current user, disabled field)
  - Member email fields (dynamic based on max_participants)
- **Validations:**
  - Team name uniqueness per event
  - Member emails must exist with 'participant' role
  - Members not already registered for the event
  - No duplicate member emails
  - Empty member fields removed
- **Session Storage:** Form data saved to session for confirmation step

#### Step 3: Registration Confirmation
- **Route:** `/events/register/<event_id>/confirm/`
- **Decorator:** `@role_required('participant')`
- **Process:**
  1. Retrieve team data from session
  2. Display team composition for review
  3. On POST:
     - Create Payment record (due: today + 3 days)
     - Create Team record
     - Create ParticipantEvent for team lead
     - Create ParticipantEvent for all members
     - Clear session data
     - Redirect to events with success message

### 4. Sponsorship System

#### Step 1: View Packages
- **Route:** `/sponsor/`
- **Decorator:** `@role_required('sponsor')`
- **Display:**
  - All sponsorship packages
  - Package categories
  - Benefits (parsed from comma-separated string)
  - Costs

#### Step 2: Select Event
- **Route:** `/sponsor/events/?package=<package_id>`
- **Decorator:** `@role_required('sponsor')`
- **Features:**
  - Display selected package details
  - List all available events
  - Event selection form

#### Step 3: Confirm Sponsorship
- **Route:** `/sponsor/confirm/` (POST)
- **Decorator:** `@role_required('sponsor')`
- **Process:**
  1. Get package and event from POST data
  2. Create or update Sponsor record using `get_or_create()`
  3. Display confirmation page
  4. Show package and event details

### 5. Dashboard System (Role-Based)

**Route:** `/dashboard/`  
**Decorator:** `@login_required`  
**Template:** Single template with conditional rendering

#### Participant Dashboard
**Data Displayed:**
- All registered events
- Team information (name, size, score)
- Team members for each event
- Event rounds (round_id, type, start_time, venue)
- Payment details

**Queries:**
```python
participant_events = ParticipantEvent.objects.filter(participant_id=user)
team_members = ParticipantEvent.objects.filter(event_id=event, team=team).exclude(participant_id=user)
event_rounds = EventRound.objects.filter(event_id=event).order_by('round_id')
```

#### Organizer Dashboard
**Data Displayed:**
- All organized events
- Participant count per event
- Team count per event
- Event rounds

**Queries:**
```python
organized_events = Event.objects.filter(organizer_id=user)
participant_count = ParticipantEvent.objects.filter(event_id=event).count()
team_count = Team.objects.filter(event=event).count()
```

#### Sponsor Dashboard
**Data Displayed:**
- All sponsored events
- Package details for each sponsorship
- Benefits breakdown

**Queries:**
```python
sponsored_events = Sponsor.objects.filter(sponsor_id=user)
```

#### Judge Dashboard
**Data Displayed:**
- All assigned events
- Event rounds for each event

**Queries:**
```python
judged_events = Event.objects.filter(judge_id=user)
event_rounds = EventRound.objects.filter(event_id=event)
```

### 6. Organizer Tools

#### View Event Participants
- **Route:** `/events/<event_id>/participants/`
- **Decorator:** `@role_required('organizer')`
- **Authorization:** Verify current user is event organizer
- **Display:**
  - All teams for the event
  - Team members in each team
  - Team captain identification
  - Team scores and payment status

**Queries:**
```python
teams = Team.objects.filter(event=event)
team_members = ParticipantEvent.objects.filter(event_id=event, team=team)
```

### 7. Data Validation & Business Logic

#### Form-Level Validations
- **SignupForm:** Password matching, email uniqueness
- **LoginForm:** Email existence check
- **TeamForm:** Team name uniqueness, member validation, duplicate check
- **EventForm:** Multi-field constraints (dates, fees, max_participants)

#### Model-Level Constraints
- Unique constraints on email, event_name, society_name
- Foreign key relationships with CASCADE/DO_NOTHING
- Composite primary keys for junction tables
- Unique together constraints

#### View-Level Logic
- Registration deadline checks
- User authorization verification
- Double-registration prevention
- Session data management

### 8. Payment System

**Automatic Payment Creation:**
- Created during team registration confirmation
- Amount: Event registration fees
- Due Date: Registration date + 3 days
- Linked to team via foreign key

**Payment Tracking:**
- Displayed on participant dashboard
- Organizers can view payment status via team details

## 💡 Implementation Details

### Design Patterns Used

#### 1. Model-View-Template (MVT)
- **Models:** Data layer with Django ORM
- **Views:** Business logic layer with function-based views
- **Templates:** Presentation layer with Django template engine

#### 2. Decorator Pattern
Custom `@role_required` decorator for authorization:
```python
def role_required(role: str):
    def require_decorator(view):
        @wraps(view)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.role != role:
                messages.error(request, f'This page is restricted to {role}')
                return redirect(request.META.get('HTTP_REFERER'))
            return view(request, *args, **kwargs)
        return wrapper
    return require_decorator
```

#### 3. Template Inheritance
- Base template with common elements
- Child templates extend and override blocks
- DRY (Don't Repeat Yourself) principle

#### 4. Session Storage Pattern
Multi-step form data preservation:
```python
# Store in session
request.session['team_form_data'] = form.cleaned_data

# Retrieve from session
cleaned_data = request.session.get('team_form_data', {})

# Clear after use
request.session.pop('team_form_data', None)
```

### Key Technical Implementations

#### 1. Custom User Model
```python
class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    role = models.CharField(max_length=20, choices=role_choices)
```
**Benefits:**
- Email-based authentication
- Role field for RBAC
- Extensible for future needs

#### 2. Dynamic Form Generation
```python
class TeamForm(forms.Form):
    def __init__(self, num_members: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in range(1, num_members):
            self.fields[f'member_{i}'] = forms.EmailField(...)
```
**Benefits:**
- Forms adapt to event requirements
- No fixed field count
- Clean validation per member

#### 3. Composite Primary Keys
```python
class ParticipantEvent(models.Model):
    pk = models.CompositePrimaryKey('participant_id', 'event_id')
    
    class Meta:
        unique_together = (('participant_id', 'event_id'),)
```
**Benefits:**
- Natural primary key
- Enforces one registration per user per event
- Efficient querying

#### 4. Get or Create Pattern
```python
sponsor_obj, created = Sponsor.objects.get_or_create(
    sponsor_id=user,
    event_id=event,
    defaults={'package': package}
)
if not created:
    sponsor_obj.package = package
sponsor_obj.save()
```
**Benefits:**
- Prevents duplicate entries
- Updates existing records
- Single database operation

#### 5. Query Optimization
```python
# Select related to avoid N+1 queries
events = Event.objects.select_related('organizer_id', 'judge_id').all()

# Order by for consistent display
events = Event.objects.all().order_by('date_time')

# Filtering with exact match
events = Event.objects.filter(category__exact=filter)
```

#### 6. Flash Message System
```python
from django.contrib import messages

messages.success(request, 'Registration successful!')
messages.error(request, 'Invalid credentials')
messages.warning(request, 'Deadline has passed')
```
**Display in Template:**
```html
{% if messages %}
    {% for message in messages %}
        <div class="alert alert-{{ message.tags }}">{{ message }}</div>
    {% endfor %}
{% endif %}
```

### Database Migration Strategy

**Migration Files:**
1. `0001_initial.py` - Initial schema creation
2. `0002_alter_user_role.py` - Modified role choices
3. `0003_alter_event_category.py` - Updated event categories
4. `0004_team_event_alter_team_team_name_and_more.py` - Team model updates
5. `0005_alter_event_event_name_and_more.py` - Event constraints

**Best Practices:**
- Small, incremental migrations
- Descriptive migration names
- Testing migrations in development
- Backup before production migrations

### URL Routing Architecture

**Root URLconf (`Nascon26/urls.py`):**
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('nascon.urls'))
]
```

**App URLconf (`nascon/urls.py`):**
- RESTful URL patterns
- Named routes for reverse lookup
- Integer converters for IDs
- Query parameters for filters

### Static File Management

**Configuration:**
```python
STATIC_URL = 'static/'
```

**Structure:**
- Global static files in app static directory
- Component-based CSS organization
- Django `{% static %}` template tag
- CDN for Font Awesome icons

### Error Handling

**Try-Except Blocks:**
```python
try:
    event = Event.objects.get(event_id=event_id)
except Event.DoesNotExist:
    messages.error(request, "Event not found.")
    return redirect('events')
```

**Form Validation Errors:**
```python
if form.is_valid():
    # Process
else:
    # Re-render with errors
```

**Authorization Checks:**
```python
if event.organizer_id != request.user:
    messages.error(request, "Not authorized")
    return redirect('dashboard')
```

## 🔒 Security Features

### 1. Authentication Security
- **Password Hashing:** bcrypt algorithm with salt
- **Session-Based Auth:** Secure session cookies
- **CSRF Protection:** Middleware-enabled CSRF tokens
- **Password Validators:**
  - UserAttributeSimilarityValidator
  - MinimumLengthValidator
  - CommonPasswordValidator
  - NumericPasswordValidator

### 2. Authorization Security
- **Role-Based Access Control:** Custom decorator enforcement
- **Login Required:** `@login_required` on protected routes
- **Ownership Verification:** Check user owns resource before allowing access
- **HTTP_REFERER Redirect:** Return to previous page on unauthorized access

### 3. Input Validation
- **Server-Side Validation:** All form inputs validated
- **SQL Injection Prevention:** Django ORM parameterized queries
- **XSS Prevention:** Template auto-escaping
- **Email Validation:** Django EmailField validation
- **Data Type Validation:** Model field type enforcement

### 4. Middleware Security
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

### 5. Database Security
- **Credentials External:** `mysql.cnf` not in version control
- **Parameterized Queries:** ORM prevents SQL injection
- **Connection Pooling:** Efficient connection management

### 6. Production Security Checklist
- [ ] `DEBUG = False`
- [ ] Strong `SECRET_KEY`
- [ ] Proper `ALLOWED_HOSTS`
- [ ] HTTPS enforcement
- [ ] Secure cookie settings
- [ ] Database backup strategy
- [ ] Rate limiting implementation
- [ ] Logging configuration

## 📸 Screenshots

*(Add screenshots of your application here)*

### Home Page
[Screenshot: Landing page with event listings]

### Event Registration
[Screenshot: Multi-step registration process]

### Dashboard Views
[Screenshot: Participant/Organizer/Sponsor/Judge dashboards]

### Admin Panel
[Screenshot: Django admin interface]

## 🚀 Future Enhancements

### Planned Features
1. **Payment Gateway Integration** - Razorpay/Stripe for online payments
2. **Email Notifications** - Registration confirmations, reminders
3. **Real-time Score Updates** - Live leaderboards for events
4. **Certificate Generation** - Automated certificate creation
5. **Accommodation Booking** - Complete accommodation module
6. **Society Features** - Full society management implementation
7. **Analytics Dashboard** - Charts and graphs for organizers
8. **Export Functionality** - CSV/PDF exports for participant lists
9. **QR Code Check-in** - Digital attendance tracking
10. **Mobile App** - React Native/Flutter companion app

### Technical Improvements
- [ ] Unit test coverage (target: 80%+)
- [ ] Integration tests for critical workflows
- [ ] API endpoints (Django REST Framework)
- [ ] Celery for background tasks
- [ ] Redis for caching
- [ ] Docker containerization
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Performance optimization (database indexing)
- [ ] WebSocket for real-time updates
- [ ] PWA features (offline support)

## 🤝 Contributors

**Development Team:**
- [Your Name] - Full Stack Developer
- [Team Member 2] - Database Designer
- [Team Member 3] - Frontend Developer
- [Team Member 4] - Backend Developer

**Academic Supervisor:**
- [Professor Name] - Database Systems Course Instructor

## 📄 License

This project is developed for educational purposes as part of the Database Systems course at [University Name]. All rights reserved.

## 📞 Contact

For questions or support:
- **Email:** [your.email@example.com]
- **GitHub:** [github.com/yourusername]
- **University:** [University Name, Department]

---

## 🙏 Acknowledgments

- Django Software Foundation for the excellent framework
- MySQL team for the robust database system
- Font Awesome for the icon library
- Stack Overflow community for troubleshooting support
- Course instructor and teaching assistants

---

**Project Status:** Active Development  
**Last Updated:** January 2026  
**Version:** 1.0.0

**Built with ❤️ using Django & MySQL**
