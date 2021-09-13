from django.urls import path
from . import views


urlpatterns = [
    path('', views.signIn, name='signIn'),
    path('signUp', views.signUp, name='signUp'),
    path('logOut', views.signOut, name='signOut'),
    path('home', views.home, name='home'),
    path('profile', views.profile, name='profile'),
]