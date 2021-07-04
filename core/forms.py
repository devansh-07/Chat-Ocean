from django import forms
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'placeholder': 'Name'}), max_length=200, required=True)
    field_order = ['username', 'first_name', 'email', 'password1', 'password2']
