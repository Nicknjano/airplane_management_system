from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.utils import timezone

from .models import Booking,Flight


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['first_name','last_name','username', 'email']

class LoginForm(AuthenticationForm):
    pass

class BookingForm(forms.ModelForm):
    CLASS_CHOICES = [
        ('Economy', 'Economy'),
        ('Business', 'Business'),
        ('First', 'First'),
    ]

    ORIGIN_CHOICES = [
        ('Nairobi', 'Nairobi'),
        ('Mombasa', 'Mombasa'),
        ('Kisumu', 'Kisumu'),
        ('Michigan', 'Michigan'),
        ('NewYork', 'New York'),
        ('California', 'California'),
    ]

    DESTINATION_CHOICES = [
        ('Nairobi', 'Nairobi'),
        ('Mombasa', 'Mombasa'),
        ('Kisumu', 'Kisumu'),
        ('Michigan', 'Michigan'),
        ('NewYork', 'New York'),
        ('California', 'California'),
    ]

    class_type = forms.ChoiceField(choices=CLASS_CHOICES)
    origin = forms.ChoiceField(choices=ORIGIN_CHOICES)
    destination = forms.ChoiceField(choices=DESTINATION_CHOICES)
    departure_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    return_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    adults = forms.IntegerField(min_value=1)
    children = forms.IntegerField(min_value=0)
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Booking
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set minimum dates dynamically
        self.fields['departure_date'].widget.attrs['min'] = str(timezone.now().date())
        self.fields['return_date'].widget.attrs['min'] = str(timezone.now().date())

    def clean(self):
        cleaned_data = super().clean()
        departure_date = cleaned_data.get('departure_date')
        return_date = cleaned_data.get('return_date')

        if return_date and return_date < departure_date:
            raise forms.ValidationError("Return date cannot be less than departure date.")

        return cleaned_data

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['flight_number', 'origin', 'destination', 'departure_date', 'departure_time', 'journey_hours', 'intervals','capacity']