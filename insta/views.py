from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, 'auth/login.html')

def signin(request):
    return render(request, 'auth/signin.html')


def home(request):
    return render(request, 'gram/index.html')

def profile(request):
    return render(request, 'gram/profile.html')