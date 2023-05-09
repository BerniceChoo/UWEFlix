from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class PaymentForm(forms.Form):
    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2)
    card_number = forms.CharField(label='Card Number')
    exp_month = forms.CharField(label='Expiration Month', max_length=2)
    exp_year = forms.CharField(label='Expiration Year', max_length=4)
    cvc = forms.CharField(label='CVC', max_length=3)
