from requests import Response
from insta.models import User, Post, Profile, CarouselImage, Like, Follow, Message,Notification,Story
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
from django.utils import timezone


def loading_page(request):
    return render(request, 'loading.html')

def error(request):
    return render(request, '404.html')

def signUp(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST['first_name']
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        
        if User.objects.filter(Q(email=email) | Q(username=username)).exists():
            messages.add_message(request, messages.ERROR, "😓 This email or username is already in use. 😓")
            return render(request, "auth/signin.html")
        if password == confirm_password:
            user = User.objects.create_user(username=username, email=email, first_name=first_name, password=password)
            messages.add_message(request, messages.SUCCESS, "🎉 Account created successfully! 🎉")
            return redirect("signIn")
        else:
            return render(request, "auth/signin.html")
        
    else:
        return HttpResponse("Method Not Allowed", status=405)
    

def signIn(request):
    try:
        if request.method == "POST":
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, "🎉 log in successfull! 🎉")
                return redirect("home")
            else:
                messages.add_message(request, messages.ERROR, "🚧 invalid infomation! 🚧", extra_tags='safe')
                return redirect("signIn")
        else:
            return render(request, "auth/login.html")
    except RequestException as e:
        print(f"An error occurred: {e}")
        return redirect("error")

@login_required(login_url='/')
def signOut(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "🎉 you have been logged out! 🎉")
    return redirect("signIn")


@login_required(login_url='/')
def upload(request):
    try:
        images = request.FILES.getlist("images")
        captions = request.POST["captions"]
        location = request.POST["location"]
        post = Post(user=request.user, location=location, captions=captions)
        post.save()

        # Link all images to the same post (carousel)
        for image in images:
            carousel_image = CarouselImage(post=post, image=image)
            carousel_image.save()
        
        messages.success(request, "🎉 Post created successfully. 🎉")
        return redirect('home') 

       
    except Exception as e:
        messages.error(request, f"Upload failed : {e}")
        return redirect('home') 


def create_story(request):
    if request.method == 'POST':
        # Process the form data and save the story
        content = request.POST.get('content')
        caption = request.POST.get('caption')
        tagged_users = request.POST.get('tagged_users')
        link = request.POST.get('link')

        if content:
            story = Story.objects.create(
                user=request.user,
                content=content,
                caption=caption,
                tagged_users=tagged_users,
                link=link,
                created_at=timezone.now()
            )
            story.save()
            return redirect('status')
    return render(request, 'gram/index.html')

def status(request):
    # stories = Story.objects.filter(expires_at__gte=timezone.now())
    user_stories = Story.objects.filter(user=request.user, expires_at__gt=timezone.now()).order_by('-created_at')
    
    if user_stories.count() > 0:
        stories = user_stories.values('content', 'caption')[:user_stories.count()]  

        context = {
            'user_stories': stories
        }
        return render(request, 'gram/status.html',context)
    else:
        messages.add_message(request, messages.ERROR, "🚧 There are no available stories! 🚧")
        return redirect("home")

def delete_story(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    if request.user == story.user:
        story.delete()
    return redirect('status')


@login_required(login_url='/')
def home(request):
    try:
        posts = Post.objects.all().order_by('-created_time').select_related('user__profile')
        profiles = Profile.objects.all() 
        current_user_profile = Profile.objects.get(user=request.user)            
        user_profile_photo_url = current_user_profile.photo.url
        other_profiles = Profile.objects.exclude(user=request.user)
        stories = Story.objects.filter(expires_at__gte=timezone.now())
        stories_with_users = Story.objects.select_related('user')
        
        
        context = {
            "posts": posts,
            "profiles": profiles,
            'profiles': other_profiles,
            'stories': stories,
            "user_profile_photo": user_profile_photo_url,
            'stories_with_users': stories_with_users  
        }
        return render(request, "gram/index.html", context)
    except RequestException as e:
        print(f"An error occurred: {e}")
        return redirect("error")


def like_toggle(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(pk=post_id)
        post.toggle_like()
        
        liked = True if post.likes > 0 else False
        data = {
            'liked': liked,
            'likes_count': post.likes,
        }
        return JsonResponse(data)
    else:
        messages.add_message(request, messages.ERROR, "🚧 Invalid request status=400 🚧")
    # JsonResponse({'error': 'Invalid request'}, )


# def post_details(request):
#     if request.method == 'GET' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest': 
#         post_id = request.GET.get('post_id')
#         try:
#             post = Post.objects.get(pk=post_id)
#             context = {
#                 "post": post 
#             }
#             return render(request, 'post_details.html', context)
#         except:
#             return JsonResponse({'error': 'Post not found'})
#     else:
#         return JsonResponse({'error': 'Invalid request'})

@login_required(login_url='/')
def post_details(request):
    if request.method == 'GET' and request.is_ajax():
        post_id = request.GET.get('post_id')
        try:
            post = Post.objects.get(pk=post_id)
            print(f"Single Image URL: {post.image.url}")
            other_profiles = Profile.objects.exclude(user=post.user)

            context = {
                "post": post,
                'profiles': other_profiles,
            }
            return render(request, 'your_app/post_details.html', context)
        except Post.DoesNotExist:
            messages.add_message(request, messages.ERROR, "🚧 Post not found status=404 🚧")
            # return JsonResponse({'error': 'Post not found'}, status=404)
        except Exception as e:
            messages.add_message(request, messages.ERROR, "🚧 internal server error status=500 🚧")
            # return JsonResponse({'error': str(e)}, status=500)
    else:
        messages.add_message(request, messages.ERROR, "🚧 Invalid request status=400 🚧")
        # return JsonResponse({'error': 'Invalid request'}, status=400)


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
        return redirect("error")


@login_required(login_url='/')
def other_profiles(request, username):
    try:
        posts = Post.objects.all().order_by('-created_time').select_related('user__profile')     
        current_user_profile = Profile.objects.get(user=request.user)
        user_profile_photo_url = current_user_profile.photo.url
        other_profiles = Profile.objects.exclude(user=request.user)
        
        context = {
            "posts": posts,
            'profiles': other_profiles,
            "user_profile_photo": user_profile_photo_url,     
        }
        return render(request, "gram/other_profile.html", context)
    except RequestException as e:
        print(f"An error occurred: {e}")
        return redirect("error")



@login_required(login_url='/')
def explore(request):
    try:
        posts = Post.objects.all().order_by('-created_time') 
        profiles = Profile.objects.all() 
        current_user_profile = Profile.objects.get(user=request.user)
       
        context = {
            "posts": posts ,
            "profiles": profiles, 
            "user_profile_photo": current_user_profile.photo.url if current_user_profile else None,
        }
        return render(request, 'gram/explore.html', context)
    except RequestException as e:
        print(f"An error occurred: {e}")
        return redirect("error")


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
            messages.add_message(request, messages.ERROR, "Form submission failed")
            # return HttpResponse("Form submission failed")
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
    profiles = Profile.objects.filter(user__username__icontains=query).values('id', 'user__username', 'photo')
    
    profiles_with_photo_urls = []
    for profile in profiles:
        photo_url = profile['photo'].url if profile['photo'] else None
        profile_data = {
            'id': profile['id'],
            'username': profile['user__username'],
            'photo_url': photo_url
        }
        profiles_with_photo_urls.append(profile_data)
    
    return JsonResponse(profiles_with_photo_urls, safe=False)



def search(request):
    query = request.GET.get('q')
    if query:
        profiles = Profile.objects.filter(user__username__icontains=query)
    else:
        profiles = Profile.objects.none()

    return render(request, 'search.html', {'profiles': profiles, 'query': query})




def notifications(request):
    user = request.user
    current_user_profile = Profile.objects.get(user=request.user)
    notifications = Notification.objects.filter(recipient=user)
    
    context = {
        'notifications': notifications,
        "user_profile_photo": current_user_profile.photo.url if current_user_profile else None,
    }
    return render(request, 'gram/notifications.html',context)

def mark_as_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.is_read = True
    notification.save()
    return redirect('notifications')