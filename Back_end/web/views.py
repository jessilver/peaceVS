from django.shortcuts import render

def home(request):
    return render(request, 'web/home.html')

def login(request):
    return render(request, 'web/login.html')

def signup(request):
    return render(request, 'web/signup.html')

# Create your views here.
