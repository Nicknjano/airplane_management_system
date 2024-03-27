"""
URL configuration for AIRLINE_MANAGEMENT_SYSTEM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from airline_management import views
from airline_management.views import index,home,booking_view,booking2,contactus,booked_flights,new_flight,manageflights,newairbus,payement,login_user,itinerary,delete_flight,add_airbus,calculate_price_view,logout_view,payment_success_pdf, payment_success

urlpatterns = [
    path('',index,name='index'),
    path('booked_flights/',booked_flights,name='booked_flights'),
    path('home/',home,name='home'),
    path('login/', login_user, name='login'),
    path('logout/', logout_view, name='logout'),
    path('booking/',booking_view,name='booking'),
    path('booking2/',booking2,name='booking2'),
    path('itinerary/',itinerary,name='itinerary'),
    path('contactus/',contactus,name='contactus'),
    path('newflight/',new_flight,name='newflight'),
    path('add_airbus/',add_airbus, name='add_airbus'),
    path('delete_flight/<int:flight_id>/',delete_flight, name='delete_flight'),
    path('calculate_price/', calculate_price_view, name='calculate_price'),
    path('manageflights/',manageflights,name='manageflights'),
    path('newairbus/',newairbus,name='newairbus'),
    path('payement/',payement,name='payement'),
    path('payment_success/', payment_success, name='payment_success'),
    path('payment_success_pdf/', payment_success_pdf, name='payment_success_pdf'),
    path("admin/", admin.site.urls),
    path('payment/initiate/<int:booking_id>/', views.initiate_payment, name='initiate_payment'),
    path('payment/execute/', views.execute_payment, name='execute_payment'),

    path('payment/cancel/', views.cancel_payment, name='cancel_payment'),
]
