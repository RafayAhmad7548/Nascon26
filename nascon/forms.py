from django import forms
from .models import User

class SignupForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'role', 'accommodation_id', 'username', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control', 'required': 'false'}),
            'accommodation_id': forms.Select(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    password_again = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
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
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError('Email not registered', code='not registered')

        return email
    
