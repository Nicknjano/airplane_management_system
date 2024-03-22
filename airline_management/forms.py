from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

from .models import Booking,Flight


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['first_name','last_name','username', 'email']

class LoginForm(AuthenticationForm):
    pass

class BookingForm(forms.Form):
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
    departure_date = forms.DateField()
    return_date = forms.DateField(required=False)
    adults = forms.IntegerField(min_value=1)
    children = forms.IntegerField(min_value=0)

    def clean(self):
        cleaned_data = super().clean()
        origin = cleaned_data.get('origin')
        destination = cleaned_data.get('destination')

        # Check if origin and destination are the same
        if origin == destination:
            raise ValidationError("Origin and destination cannot be the same.")
        
        return cleaned_data

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['flight_number', 'origin', 'destination', 'departure_date', 'departure_time', 'journey_hours', 'intervals','capacity']