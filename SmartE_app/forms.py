from django import forms
from .models import Membership

class RegistrationForm(forms.Form):
    sid = forms.CharField(max_length=10)
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    membership_type = forms.ModelChoiceField(queryset=Membership.objects.all())

class PaymentForm(forms.Form):
    membership_type = forms.ModelChoiceField(queryset=Membership.objects.all())
    name = forms.CharField(max_length=100)
    cardnumber = forms.CharField(max_length=16)
    expiry = forms.CharField(max_length=5)
    cvv = forms.CharField(max_length=4)