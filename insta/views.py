from requests import Response
from insta.models import User, Post, Profile, CarouselImage, Like, Follow, Message
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from .forms import ProfileForm, MessageForm
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch, Q, Subquery, OuterRef, Count
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from requests.exceptions import RequestException
from django.conf import settings


def signUp(request):
    try:
        if request.method == "POST":
            username = request.POST["username"]
            email = request.POST["email"]
            first_name = request.POST['first_name']
            password = request.POST["password"]
            confirm_password = request.POST["confirm_password"]
            
            if User.objects.filter(Q(email=email) | Q(username=username)).exists():
                messages.add_message(request, messages.ERROR, "This email or username is already in use.")
                return render(request, "auth/signin.html")
            if password == confirm_password:
                user = User(
                    username=username, email=email, first_name= first_name, password=make_password(password)
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


@login_required(login_url='/')
def upload(request):
    try:
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
        
        return JsonResponse({'message': 'Post created successfully.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required(login_url='/')
def home(request):
    try:
        posts = Post.objects.all().order_by('-created_time').select_related('user__profile')
        
        likes_prefetch = Prefetch('like_set', queryset=Like.objects.filter(user=request.user), to_attr='user_likes')
        posts = posts.prefetch_related(likes_prefetch)
        
        profiles = Profile.objects.all() 
        
        current_user_profile = Profile.objects.get(user=request.user)
        for post in posts:
            for carousel_image in post.carouselimage_set.all():
                print(f"Carousel Image URL: {carousel_image.image.url}")
            print(f"Single Image URL: {post.image.url}")
            
        user_profile_photo_url = current_user_profile.photo.url
        for post in posts:
            post.liked = any(like.is_like for like in getattr(post, 'user_likes', []))

        
        other_profiles = Profile.objects.exclude(user=request.user)
        
        context = {
            "posts": posts,
            "profiles": profiles,
            'profiles': other_profiles,
            "user_profile_photo": user_profile_photo_url, 
            # "user_profile_photo": current_user_profile.photo.url if current_user_profile else None,    
        }
        return render(request, "gram/index.html", context)
    except RequestException as e:
        print(f"An error occurred: {e}")
        return render(request, "connection_error.html")


def like_toggle(request, post_id):
    if request.method == 'POST' and request.user.is_authenticated:
        post = get_object_or_404(Post, pk=post_id)
        like, created = Like.objects.get_or_create(post=post, user=request.user)

        context = {
                "post": post,   
        }
    
        if created:
            like.is_like = True
            like.save()
            return JsonResponse({'liked': True})
        else:
            like.is_like = not like.is_like
            like.save()
            return JsonResponse({'liked': like.is_like}) 
        
    else:
        return JsonResponse({}, status=400) 
   

@login_required(login_url='/')
def viewImage(request, pk):
    try:
        post = Post.objects.get(id=pk)
        if request.method == "POST":            
            if post.user == request.user:
                post.delete()
            return redirect('home')
        
        return render(request, "gram/viewImage.html", {"post": post})
    except RequestException as e:
        print(f"An error occurred: {e}")
        return render(request, "connection_error.html")

@login_required(login_url='/')
def profile(request):
    try:
        profiles = Profile.objects.all()
        posts = Post.objects.filter(user=request.user)

        if request.method == "POST":
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                current_user = request.user
                new_photo = form.cleaned_data['photo'] 
                new_bio = form.cleaned_data['bio']  

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
            current_user_profile = Profile.objects.get(user=request.user) 

            # Count the number of followers for the current user
            followers_count = Follow.objects.filter(following=request.user).count()

            # Count the number of users the current user is following
            following_count = Follow.objects.filter(follower=request.user).count()

        except Profile.DoesNotExist:
            # Handle the case where the profile doesn't exist
            current_user_profile = None
            followers_count = 0
            following_count = 0
            
        user_posts = Post.objects.filter(user=request.user)
        
        if current_user_profile and current_user_profile.photo:
            user_profile_photo_url = current_user_profile.photo.url
        else:
            user_profile_photo_url = settings.DEFAULT_PROFILE_PHOTO_URL
            

        # profile_user = User.objects.get(username=username)
        # is_following = False
        # if request.user.is_authenticated:
        #     is_following = request.user.profile.following.filter(id=profile_user.id).exists()

        context = {
            "profiles": profiles,
            "post": posts,
            "form": form,
            # 'is_following': is_following,
            'user_posts': user_posts,
            "followers_count": followers_count,
            "following_count": following_count,
            "user_profile_photo": user_profile_photo_url,    
        }

        return render(request, "gram/profile.html", context)
    
    except RequestException as e:
        print(f"An error occurred: {e}")
        return render(request, "connection_error.html")

@login_required(login_url='/')
def explore(request):
    try:
        posts = Post.objects.all().order_by('-created_time') 
        profiles = Profile.objects.all() 
        current_user_profile = Profile.objects.get(user=request.user)
        for post in posts:
            for carousel_image in post.carouselimage_set.all():
                print(f"Carousel Image URL: {carousel_image.image.url}")
            print(f"Single Image URL: {post.image.url}")

        context = {"posts": posts ,"profiles": profiles, 
             "user_profile_photo": current_user_profile.photo.url if current_user_profile else None,}
        return render(request, 'gram/explore.html', context)
    except RequestException as e:
        print(f"An error occurred: {e}")
        return render(request, "connection_error.html")


def follow_user(request, username):
    if request.user.is_authenticated:
        follower = request.user
        following_user = User.objects.get(username=username)

        if follower != following_user:  # Prevent self-following
            follow_instance, created = Follow.objects.get_or_create(follower=follower, following=following_user)
            if not created:
                # User is already following, maybe show a message
                pass
    return redirect('user_profile', username=username)

def unfollow_user(request, username):
    if request.user.is_authenticated:
        follower = request.user
        following_user = User.objects.get(username=username)
        Follow.objects.filter(follower=follower, following=following_user).delete()
    return redirect('user_profile', username=username)


def inbox(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('inbox')
        else:
            return HttpResponse("Form submission failed")
    else:
        form = MessageForm()
        current_user_profile = Profile.objects.get(user=request.user)
        received_messages = Message.objects.filter(receiver=request.user)
        latest_messages = Message.objects.filter(sender=request.user, receiver=OuterRef('receiver')).order_by('-timestamp')
        latest_message_ids = latest_messages.values('id')[:1]
        sent_messages = Message.objects.filter(sender=request.user, id__in=Subquery(latest_message_ids)).select_related('receiver', 'receiver__profile')

        # all_messages = sent_messages | received_messages
        all_messages = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
        
        context = {
            'form': form,
            'received_messages': received_messages,
            'sent_messages': sent_messages, 
            'all_messages': all_messages,
            "user_profile_photo": current_user_profile.photo.url if current_user_profile else None,
        }
        return render(request, 'gram/inbox.html', context)



def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.sender == request.user or message.receiver == request.user:
        message.delete()
    return redirect('inbox')

def clear_messages(request):
    messages_to_delete = Message.objects.filter(sender=request.user)
    messages_to_delete.delete()
    return redirect('inbox')




def search_profiles(request):
    query = request.GET.get('q')
    profiles = User.objects.filter(username__icontains=query).values('id', 'username')
    return JsonResponse(list(profiles), safe=False)




def search(request):
    query = request.GET.get('q')

    if query:
        profiles = Profile.objects.filter(user__username__icontains=query)
    else:
        profiles = Profile.objects.none()

    return render(request, 'search.html', {'profiles': profiles, 'query': query})