from insta.models import Users
from django.shortcuts import render
# from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def login(request):
    return render(request, 'auth/login.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            user = Users(username=username, email=email, password=password)
        else:
            print("password")
    else:
        return render(request, 'auth/signin.html')
def home(request):
    return render(request, 'gram/index.html')

def profile(request):
    return render(request, 'gram/profile.html')