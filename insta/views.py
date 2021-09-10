from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, 'gram/login.html')


def signin(request):
    return render(request, 'gram/signin.html')