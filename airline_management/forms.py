from django import forms
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

from .models import Booking,Flight


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['first_name','last_name','username', 'email']

class LoginForm(AuthenticationForm):
    pass

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'


class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['flight_number', 'origin', 'destination', 'departure_date', 'departure_time', 'journey_hours', 'intervals']