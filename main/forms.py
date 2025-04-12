from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Item, Claim

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'category', 'status', 'location', 
                 'date_occurred', 'image', 'contact_info', 'additional_notes']
        widgets = {
            'date_occurred': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'additional_notes': forms.Textarea(attrs={'rows': 4}),
        }

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['description', 'proof_of_ownership']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'proof_of_ownership': forms.Textarea(attrs={'rows': 4}),
        } 