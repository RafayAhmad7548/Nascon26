from datetime import date, datetime, timedelta
from django import forms
from django.forms.widgets import EmailInput
from .models import Event, ParticipantEvent, Team, User

class SignupForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'role', 'username', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control', 'required': 'false'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    password_again = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['username'].help_text = ''

    def clean(self):
        super().clean()

        password = self.cleaned_data.get('password')
        password_again = self.cleaned_data.get('password_again')

        if password != password_again:
            raise forms.ValidationError(('Passwords don\'t match'), code='invalid')
    
    # to ensure proper hashing
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
        


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError('Email not registered', code='not registered')

        return email
 

class TeamForm(forms.Form):
    team_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    event = forms.IntegerField(widget=forms.HiddenInput())
    team_lead =  forms.EmailField(max_length=255, disabled=True, widget=forms.EmailInput(attrs={'class': 'form-control',}))

    def __init__(self, num_members: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_members = num_members
        
        for i in range(1, self.num_members):
            self.fields[f'member_{i}'] = forms.EmailField(max_length=255, required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean(self):
        super().clean()
        
        team_name = self.cleaned_data.get('team_name')
        event = self.cleaned_data.get('event')
        try:
            Team.objects.get(team_name=team_name, event=event)
            self.add_error('team_name', forms.ValidationError('Team name not available', code='not available'))
        except Team.DoesNotExist:
            members = []
            # remove empty fields
            for i in range(1, self.num_members):
                member = self.cleaned_data.get(f'member_{i}')
                if member == '':
                    self.cleaned_data.pop(f'member_{i}')
                else:
                    try:
                        user = User.objects.get(email=member, role='participant')
                        ParticipantEvent.objects.get(pk=(user.id, event)) # type: ignore
                        self.add_error(f'member_{i}', error=forms.ValidationError('Participant already registered for this event'))
                    except User.DoesNotExist:
                        self.add_error(f'member_{i}', error=forms.ValidationError('Participant does not exist'))
                    except ParticipantEvent.DoesNotExist:
                        members.append(member)

            if len(members) != len(set(members)):
                raise forms.ValidationError('Team members must be unique', code='must be unique')


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'description', 'category', 'max_participants', 'registration_fees', 'registration_last_date', 'date_time']
        widgets = {
            'event_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control', 'required': 'false'}),
            'max_participants': forms.NumberInput(attrs={'class': 'form-control'}),
            'registration_fees': forms.NumberInput(attrs={'class': 'form-control'}),
            'registration_last_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
        }

    judge = forms.EmailField(widget=EmailInput(attrs={'class': 'form-control'}))


    def clean_max_participants(self):
        max_participants = self.cleaned_data.get('max_participants')
        if max_participants:
            if max_participants < 1 or max_participants > 12:
                raise forms.ValidationError('max participants should be between 1 and 12', code='out of range')
        
        return max_participants

    def clean_registration_fees(self):
        registration_fees = self.cleaned_data.get('registration_fees')
        if registration_fees:
            if registration_fees % 10 != 0:
                raise forms.ValidationError('fees must be divisible by 10')
            if registration_fees < 500:
                raise forms.ValidationError('minium fees is 500')
            if registration_fees > 5000:
                raise forms.ValidationError('maximum fees is 5000')

        return registration_fees

    def clean_registration_last_date(self):
        registration_last_date = self.cleaned_data.get('registration_last_date')
        if registration_last_date:
            if registration_last_date < timedelta(days=3) + date.today():
                raise forms.ValidationError('last date for registration must be at least 3 days from now')

        return registration_last_date
    
    def clean_judge(self):
        judge = self.cleaned_data.get('judge')

        try:
            judge = User.objects.get(email=judge, role='judge')
        except User.DoesNotExist:
            raise forms.ValidationError('no judge with this email exists')

        return judge
    
    def clean(self):
        super().clean()

        registration_last_date = self.cleaned_data.get('registration_last_date')
        date_time = self.cleaned_data.get('date_time')
        
        if registration_last_date and date_time:
            tz = date_time.tzinfo
            if date_time < datetime.combine(registration_last_date + timedelta(days=3), datetime.min.time(), tzinfo=tz):
                self.add_error('date_time', forms.ValidationError('Event date should be at least 3 days from last registration date'))
        
    
    
    



