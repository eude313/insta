from insta.models import Users, Post, Profile
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

def upload(request):
    if request.method == "POST":
        image= request.FILES['image']
        captions = request.POST['captions']
        post= Post(author=request.user, image=image, captions=captions)
        post.save()
        return redirect("home")
    else:
        return render(request, 'gram/upload.html')


def home(request):
    posts = Post.objects.all()
    context= {'posts':posts}
    return render(request, 'gram/index.html', context)

def viewImage(request, pk):
    posts = Post.objects.get(id=pk)
    if request.method == 'POST':
        posts.delete()
        return redirect('home')
    return render(request, 'gram/viewImage.html', {'post':posts})

def profile(request):
    profiles = Profile.objects.all()
    posts = Post.objects.all()
    if request.method == 'POST':
        photo= request.FILES['photo']
        gender= request.POST['gender']
        bio = request.POST['bio']
        profile= Profile(photo=photo, bio=bio, gender=gender)
        profile.save()
        return redirect("profile")
    context= {'profiles':profiles, 'post':posts }
    return render(request, 'gram/profile.html', context)
