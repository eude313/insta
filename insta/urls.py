from django.urls import path
from . import views


urlpatterns = [
    path('', views.signIn, name='signIn'),
    path('signUp', views.signUp, name='signUp'),
    path('logOut', views.signOut, name='signOut'),
    path('home', views.home, name='home'),
    path('viewImage/<str:pk>/', views.viewImage, name='viewImage'),
    path('profile', views.profile, name='profile'),
    path('upload', views.upload, name='upload'),
]