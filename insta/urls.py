from django.urls import path
from . import views


urlpatterns = [
    path("", views.signIn, name="signIn"),
    path("signUp", views.signUp, name="signUp"),
    path("logOut", views.signOut, name="signOut"),
    path("home", views.home, name="home"),
    path("viewImage/<str:pk>/", views.viewImage, name="viewImage"),
    path("profile", views.profile, name="profile"),
    path("upload", views.upload, name="upload"),
    path('explore/', views.explore, name='explore'),
    
    # path('follow/<str:username>/', views.user_follow, name='user_follow'),
    # path('unfollow/<str:username>/', views.user_unfollow, name='user_unfollow'),
]
