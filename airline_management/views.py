from django.shortcuts import render

def index(request):
    return render(request,'index.html')
def home(request):
    return render(request,'home.html')
def booking(request):
    return render(request,'booking.html')
def contactus(request):
    return render(request,'contactus.html')
