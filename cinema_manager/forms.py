from django import forms
from django.forms import ModelForm
from .models import Club

class ClubForm(ModelForm):
    class Meta:
        model = Club
        
        fields = ('club_name', 'club_address_number', 'club_address_street', 'club_address_city', 'club_address_postcode', 'club_tphone' , 'club_phone', 'club_email', 'rep_first_name', 'rep_last_name', 'rep_dob', 'image')

        widgets = {
            'club_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Club Name'}),
            'club_address_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Number'}),
            'club_address_street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street'}),
            'club_address_city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'club_address_postcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Club Address Postcode'}),
            'club_tphone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Club Telephone No.'}),
            'club_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Club Phone No.'}),
            'club_email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Club Email'}),
            'rep_first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Representative First Name'}),
            'rep_last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Representative Last Name'}),
            'rep_dob': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Representative Date of Birth (DD/MM/YYYY)'}),
        }