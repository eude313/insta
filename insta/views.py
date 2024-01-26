from insta.models import User, Post, Profile, CarouselImage
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from .forms import ProfileForm 
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from requests.exceptions import RequestException

def signUp(request):
    try:
        if request.method == "POST":
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]
            confirm_password = request.POST["confirm_password"]
            
            if User.objects.filter(Q(email=email) | Q(username=username)).exists():
                messages.add_message(request, messages.ERROR, "This email or username is already in use.")
                return render(request, "auth/signin.html")
            if password == confirm_password:
                user = User(
                    username=username, email=email, password=make_password(password)
                )
                user.save()
                messages.add_message(
                    request, messages.SUCCESS, "Account created successfully!"
                )
                return redirect("signIn")
            else:
                print("wrong password")
        return render(request, "auth/signin.html")
    except RequestException as e:
        print(f"An error occurred: {e}")
        return render(request, "connection_error.html")




def signIn(request):
    try:
        if request.method == "POST":
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, "log in successfull!")
                return redirect("home")
            else:
                messages.add_message(request, messages.ERROR, "invalid infomation!")
                return redirect("signIn")
        else:
            return render(request, "auth/login.html")
    except RequestException as e:
        print(f"An error occurred: {e}")
        return render(request, "connection_error.html")

def signOut(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "you have been logged Out!")
    return redirect("signIn")


def upload(request):
    try:
        if request.method == "POST":
            images = request.FILES.getlist("images")
            captions = request.POST["captions"]
            location = request.POST["location"]
            # Create one post for the carousel
            post = Post(user=request.user, location=location, captions=captions)
            post.save()

            # Link all images to the same post (carousel)
            for image in images:
                carousel_image = CarouselImage(post=post, image=image)
                carousel_image.save()
            return redirect("home")
        else:
            return render(request, "gram/upload.html")
    except RequestException as e:
        print(f"An error occurred: {e}")
        return render(request, "connection_error.html")

@login_required(login_url='/')
def home(request):
    try:
        posts = Post.objects.all().order_by('-created_time') 
        profiles = Profile.objects.all() 
        current_user_profile = Profile.objects.get(user=request.user)
        for post in posts:
            for carousel_image in post.carouselimage_set.all():
                print(f"Carousel Image URL: {carousel_image.image.url}")
            print(f"Single Image URL: {post.image.url}")
        
        context = {
            "posts": posts,
            "profiles": profiles,
            "user_profile_photo": current_user_profile.photo.url if current_user_profile else None,    
        }
        return render(request, "gram/index.html", context)
    except RequestException as e:
        print(f"An error occurred: {e}")
        return render(request, "connection_error.html")

@login_required(login_url='/')
def viewImage(request, pk):
    try:
        posts = Post.objects.get(id=pk)
        if request.method == "POST":
            posts.delete()
            return redirect("home")
        return render(request, "gram/viewImage.html", {"post": posts})
    except RequestException as e:
        print(f"An error occurred: {e}")
        return render(request, "connection_error.html")

@login_required(login_url='/')
def profile(request):
    try:
        profiles = Profile.objects.all()
        posts = Post.objects.all()

        if request.method == "POST":
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                current_user = request.user
                new_photo = form.cleaned_data['photo']  # Adjust this based on your form field name
                new_bio = form.cleaned_data['bio']  # Adjust this based on your form field name

                try:
                    # Update the existing profile
                    current_user_profile = Profile.objects.get(user=current_user)
                    current_user_profile.photo = new_photo
                    current_user_profile.bio = new_bio
                    current_user_profile.save()
                except Profile.DoesNotExist:
                    # Create a new profile
                    Profile.objects.create(user=current_user, photo=new_photo, bio=new_bio)

                return redirect("profile")
        else:
            form = ProfileForm()

        try:
            # Try to get the current user's profile
            current_user_profile = Profile.objects.get(user=request.user)
            followers_count = current_user_profile.followers.count()
            following_count = current_user_profile.following.count()
        except Profile.DoesNotExist:
            # If the profile does not exist, handle this case (you might redirect to a profile creation page)
            current_user_profile = None
            followers_count = 0
            following_count = 0
            
        current_user_profile = Profile.objects.get(user=request.user)
        followers_count = current_user_profile.followers.count()
        following_count = current_user_profile.following.count()
        user_posts = Post.objects.filter(user=request.user)

        context = {
            "profiles": profiles,
            "post": posts,
            "form": form,
            'user_posts': user_posts,
            "followers_count": followers_count,
            "following_count": following_count,
            "user_profile_photo": current_user_profile.photo.url if current_user_profile else None,    }

        return render(request, "gram/profile.html", context)
    
    except RequestException as e:
        print(f"An error occurred: {e}")
        return render(request, "connection_error.html")

@login_required(login_url='/')
def explore(request):
    try:
        posts = Post.objects.all().order_by('-created_time') 
        for post in posts:
            for carousel_image in post.carouselimage_set.all():
                print(f"Carousel Image URL: {carousel_image.image.url}")
            print(f"Single Image URL: {post.image.url}")
        context = {"posts": posts}
        return render(request, 'gram/explore.html', context)
    except RequestException as e:
        print(f"An error occurred: {e}")
        return render(request, "connection_error.html")

# @login_required
# def user_posts(request):
#     try:
#         user_posts = Post.objects.filter(user=request.user)
#         context = {'user_posts': user_posts}
#         return render(request, 'user_posts.html', context)
#     except RequestException as e:
#         print(f"An error occurred: {e}")
#         return render(request, "connection_error.html")

# @login_required
# def user_follow(request, username):
#     user_to_follow = get_object_or_404(User, username=username)
#     profile_to_follow = user_to_follow.profile
#     request.user.profile.followers.add(profile_to_follow.user)
#     return JsonResponse({'status': 'ok'})

# @login_required
# def user_unfollow(request, username):
#     user_to_unfollow = get_object_or_404(User, username=username)
#     profile_to_unfollow = user_to_unfollow.profile
#     request.user.profile.followers.remove(profile_to_unfollow.user)
#     return JsonResponse({'status': 'ok'})