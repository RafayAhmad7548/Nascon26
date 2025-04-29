from django import forms
from .models import User

class SignupForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'role', 'accommodation_id', 'username', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'accommodation_id': forms.Select(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    password_again = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''

    def clean(self):
        super().clean()

        password = self.cleaned_data.get('password')
        password_again = self.cleaned_data.get('password_again')

        if password != password_again:
            raise forms.ValidationError(('passwords don\'t match'), code='invalid')
    
    # to ensure proper hashing
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
        

# class SignupForm(forms.Form):
#     username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     role = forms.ChoiceField(choices=[('Participant', 'Participant'), ('Sponsor', 'Sponsor')], 
#                             widget=forms.RadioSelect)
#
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")
#
#         if password != confirm_password:
#             raise forms.ValidationError("Passwords don't match")
#
#         # Check if username is already taken
#         username = cleaned_data.get("username")
#         if User.objects.filter(username=username).exists():
#             raise forms.ValidationError("Username is already taken")
#
#         # Check if email is already taken
#         email = cleaned_data.get("email")
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError("Email is already registered")
#
#         return cleaned_data
#
# class LoginForm(forms.Form):
#     username_or_email = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
