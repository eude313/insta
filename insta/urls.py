from django.urls import path
from . import views


urlpatterns = [
    path("", views.signIn, name="signIn"),
    path("signUp", views.signUp, name="signUp"),
    path("logOut", views.signOut, name="signOut"),
    path("home", views.home, name="home"),
    # path("viewImage/<str:pk>/", views.viewImage, name="viewImage"),
    path("profile/", views.profile, name="profile"),
    path("upload", views.upload, name="upload"),
    path('explore/', views.explore, name='explore'),
    path('inbox/', views.inbox, name='inbox'),
    path('search/', views.search, name='search'),
 
    path('like_toggle/', views.like_toggle, name='like_toggle'),

    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow_user'),


    path('message/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('messages/clear/', views.clear_messages, name='clear_messages'),
    path('search/profiles/', views.search_profiles, name='search_profiles'),
    
    
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark_as_read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
] 
