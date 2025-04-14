from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Item, Claim

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['full_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'category', 'status', 'location', 'date_occurred', 'image', 'contact_info', 'additional_notes']
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