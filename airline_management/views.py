
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SignupForm,LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse,JsonResponse
from django.contrib import messages

from .forms import BookingForm,FlightForm
from django.http import JsonResponse
from .models import Flight, Airbus, Booking,Route

import json
import paypalrestsdk
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from paypalrestsdk import Payment
from .models import Booking


from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Booking  # Import the Booking model

def send_itinerary_email(request, booking_id):
    booking = Booking.objects.get(id=booking_id)

    # Render the itinerary HTML template to a string
    itinerary_html = render_to_string('itinerary.html', {'form': booking})

    # Extract plaintext from HTML for the email body
    itinerary_text = strip_tags(itinerary_html)

    # Print the itinerary text (for debugging)
    print("Itinerary Text:")
    print(itinerary_text)

    # Print the itinerary HTML (for debugging)
    print("Itinerary HTML:")
    print(itinerary_html)

    # Send email with itinerary details
    send_mail(
        'Your Flight Itinerary',
        itinerary_text,
        'skyops34@gmail.com',  # Change this to your sender email address
        [booking.email],  # Send to the email specified in the booking
        html_message=itinerary_html,
    )


def initiate_payment(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    total_price = booking.price

    paypalrestsdk.configure({
        "mode": "sandbox",  # Change to "live" in production
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_SECRET_KEY,
    })

    payment = Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('execute_payment')),
            "cancel_url": request.build_absolute_uri(reverse('cancel_payment')),
        },
        "transactions": [{
            "amount": {
                "total": str(total_price),
                "currency": "USD"
            },
            "description": "Flight Booking"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = str(link.href)
                return redirect(redirect_url)
    else:
        return HttpResponse("Payment creation failed")

def execute_payment(request):
    payment_id = request.GET.get("paymentId")
    payer_id = request.GET.get("PayerID")

    payment = Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        # Update booking payment status
        booking_id = request.session.get('booking_id')
        if booking_id:
            booking = Booking.objects.get(id=booking_id)
            booking.payment_status = 'paid'
            booking.save()
        
        # Retrieve necessary data from the session
        itinerary_data = request.session.get('itinerary_data', {})
        
        # Render the payment success template with necessary data
        return render(request, 'payment_success.html', itinerary_data)
    else:
        # Optionally, you can pass any additional context data to the template
        return render(request, 'payment_success.html')



def cancel_payment(request):
    return HttpResponse("Payment cancelled")


def home(request):
    # Get the logged-in user
    logged_in_user = request.user
    
    return render(request, 'home.html', {'logged_in_user': logged_in_user})
@login_required
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
@login_required
def newairbus(request):
    airbuses = Airbus.objects.all()
    return render(request, 'newairbus.html', {'airbuses': airbuses})
@login_required
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
@login_required
def manageflights(request):
    flights = Flight.objects.all()  # Retrieve all flights from the database
    return render(request, 'manageflights.html', {'flights': flights})
@login_required
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
            booking = form.save(commit=False)
            booking.origin = form.cleaned_data['origin']
            booking.destination = form.cleaned_data['destination']
            booking.departure_date = form.cleaned_data['departure_date']
            booking.return_date = form.cleaned_data['return_date']
            booking.adults = form.cleaned_data['adults']
            booking.children = form.cleaned_data['children']
            
            # Calculate the price and save it to the booking
            booking.price = calculate_price(booking.origin, booking.destination, booking.adults)
            booking.save()

            # Prepare data to be passed to the itinerary template
            adult_passengers = []
            for i in range(booking.adults):
                full_name = request.POST.get(f'full_name_{i}', '')
                email = request.POST.get(f'email_{i}', '')
                adult_passengers.append({'full_name': full_name, 'email': email})

            # Render the itinerary template with the relevant data
            return render(request, 'itinerary.html', {'form': form, 'booking': booking, 'adult_passengers': adult_passengers})
        else:
            print("Form errors:", form.errors)
            return render(request, 'booking.html', {'form': form})
    else:
        form = BookingForm()
        return render(request, 'booking.html', {'form': form})



def calculate_price(origin, destination, adults):
    try:
        # Retrieve the route object from the database based on origin and destination
        route = Route.objects.get(origin=origin, destination=destination)
        # Get the price from the route object
        price = route.price
        # Calculate total price based on the number of adults
        total_price = price * adults
        return total_price
    except Route.DoesNotExist:
        # Handle the case where the route does not exist
        return None
    
def calculate_price_view(request):
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')
    adults = int(request.GET.get('adults', 0))  # Ensure adults is an integer
    
    price = calculate_price(origin, destination, adults)
    
    return JsonResponse({'price': price})

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
@login_required
def home(request):
    return render(request,'home.html')
def booking2(request):
    return render(request,'booking2.html')
def contactus(request):
    return render(request,'contactus.html')
@login_required
def booked_flights(request):
    bookings = Booking.objects.all()
    return render(request, 'booked_flights.html', {'bookings': bookings})

def payement(request):
    return render(request,'payement.html')
# def itinerary(request, **kwargs):
#     return render(request, 'itinerary.html', kwargs)
def itinerary(request, **kwargs):
    if request.method == 'POST':
        adult_passengers = request.POST.get('adult_passengers')
        # Convert JSON string to Python object
        adult_passengers = json.loads(adult_passengers)
        # Store necessary data in the session
        request.session['itinerary_data'] = {
            'adult_passengers': adult_passengers,
            # Add any other data you want to pass to the payment success page
        }
        return render(request, 'itinerary.html', {'adult_passengers': adult_passengers})
    # Handle GET requests if needed
    return render(request, 'itinerary.html')


def logout_view(request):
    logout(request)
    return redirect('index')