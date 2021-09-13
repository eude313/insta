from insta.models import Users, Post
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def signUp(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            user = Users(username=username, email=email, password=make_password(password))
            user.save()
            messages.add_message(request, messages.SUCCESS, "Account created successfully!")
            return redirect("signIn")
        else:
            print("wrong password")
    return render(request, 'auth/signin.html')

def signIn(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, "Successfully logged in!")
            return redirect("home")
        else:
            messages.add_message(request, messages.ERROR, "invalid infomation!") 
            return redirect("signIn")  
    else:
        return render(request, 'auth/login.html')
    
def signOut(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Successfully logged Out!")
    return redirect("signIn") 

def home(request):
    
    return render(request, 'gram/index.html')

def profile(request):
    return render(request, 'gram/profile.html')