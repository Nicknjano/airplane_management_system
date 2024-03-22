
from django.shortcuts import render,redirect,get_object_or_404
from .forms import SignupForm,LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse,JsonResponse
from django.contrib import messages

from .forms import BookingForm,FlightForm
from django.http import JsonResponse
from .models import Flight, Airbus, Booking

def add_airbus(request):
    if request.method == 'POST':
        airbus_no = request.POST.get('airbus_no')
        capacity = request.POST.get('capacity')
        
        # Create a new Airbus instance
        Airbus.objects.create(airbus_no=airbus_no, capacity=capacity)
        
        # Redirect to a success page or another appropriate view
        return redirect('newairbus')
    else:
        # Handle GET requests if needed
        pass

def newairbus(request):
    airbuses = Airbus.objects.all()
    return render(request, 'newairbus.html', {'airbuses': airbuses})

def delete_flight(request, flight_id):
    # Retrieve the flight object from the database
    flight = get_object_or_404(Flight, pk=flight_id)

    if request.method == 'POST':
        # If the request is a POST request, delete the flight
        flight.delete()
        # Redirect to a success URL, such as the manage flights page
        return redirect('manageflights')
    else:
        # If the request is not a POST request, render a confirmation template
        return render(request, 'confirm_delete_flight.html', {'flight': flight})

def manageflights(request):
    flights = Flight.objects.all()  # Retrieve all flights from the database
    return render(request, 'manageflights.html', {'flights': flights})

def new_flight(request):
    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manageflights')
    else:
        form = FlightForm()
    return render(request, 'newflight.html', {'form': form})


def booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Access cleaned data from the form
            class_type = form.cleaned_data['class_type']
            origin = form.cleaned_data['origin']
            destination = form.cleaned_data['destination']
            departure_date = form.cleaned_data['departure_date']
            return_date = form.cleaned_data['return_date']
            adults = form.cleaned_data['adults']
            children = form.cleaned_data['children']

            # Create a new Booking instance and save it
            booking = Booking(
                class_type=class_type,
                origin=origin,
                destination=destination,
                departure_date=departure_date,
                return_date=return_date,
                adults=adults,
                children=children
            )
            booking.save()

            # Redirect to a success page or render a success message
            return redirect('itinerary')
        else:
            # Render the form with validation errors
            print("Form errors:", form.errors)
            return render(request, 'booking.html', {'form': form})
    else:
        form = BookingForm()
        return render(request, 'booking.html', {'form': form})


def create_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return HttpResponse("User with this username already exists.")
        
        # Create the user
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)  # Encrypt the password
        )
        
        return HttpResponse("User created successfully.")
    else:
        return HttpResponse("Invalid request method.")
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user) 
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form}) 
def index(request):
    return render(request,'index.html')
def home(request):
    return render(request,'home.html')
def booking2(request):
    return render(request,'booking2.html')
def contactus(request):
    return render(request,'contactus.html')
def user(request):
    return render(request,'user.html')
def accounts(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({'message': 'User with this username already exists.'})
        
        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password  # Django handles password hashing
        )
        
        if user:
            return JsonResponse({'message': 'User created successfully.'})
        else:
            return JsonResponse({'message': 'Failed to create user.'}, status=500)
    
    return render(request, 'accounts.html')
def payement(request):
    return render(request,'payement.html')
def itinerary(request):
    return render(request,'itinerary.html')