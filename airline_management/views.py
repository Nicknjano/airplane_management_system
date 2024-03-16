from django.shortcuts import render

def index(request):
    return render(request,'index.html')
def home(request):
    return render(request,'home.html')
def booking(request):
    return render(request,'booking.html')
def contactus(request):
    return render(request,'contactus.html')
def user(request):
    return render(request,'user.html')
def newflight(request):
    return render(request,'newflight.html')
def manageflights(request):
    return render(request,'manageflights.html')
def newairbus(request):
    return render(request,'newairbus.html')
def accounts(request):
    return render(request,'accounts.html')