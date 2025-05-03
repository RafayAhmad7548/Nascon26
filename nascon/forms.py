from django import forms
from django.db.models import Q
from django.db.models.utils import make_model_tuple
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
                        members.append(member)
                    except User.DoesNotExist:
                        self.add_error(f'member_{i}', error=forms.ValidationError('Participant does not exist'))
                    except ParticipantEvent.DoesNotExist:
                        self.add_error(f'member_{i}', error=forms.ValidationError('Participant already registered for this event'))

            if len(members) != len(set(members)):
                raise forms.ValidationError('Team members must be unique', code='must be unique')
        
