from django.urls import path
from . import views



urlpatterns = [
    path('', views.loading_page, name='loading_page'),
    path("signIn", views.signIn, name="signIn"),
    path('error/', views.error, name='error'),
    path('signUp/', views.signUp, name='signUp'),
    
    path("logOut", views.signOut, name="signOut"),
    path("home", views.home, name="home"),
    # path("viewImage/<str:pk>/", views.viewImage, name="viewImage"),
    path("profile/", views.profile, name="profile"),
    path("upload", views.upload, name="upload"),
    path('explore/', views.explore, name='explore'),
    path('inbox/', views.inbox, name='inbox'),
    path('search/', views.search, name='search'),
    path('create_story/', views.create_story, name='create_story'),
    path('status/', views.status, name='status'),
    
    path('post_details/', views.post_details, name='post_details'),
 
    path('like_toggle/', views.like_toggle, name='like_toggle'),

    path('other_profiles/', views.other_profiles, name='other_profiles'),    

    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow_user'),


    path('message/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('messages/clear/', views.clear_messages, name='clear_messages'),
    path('search/profiles/', views.search_profiles, name='search_profiles'),
    
    
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark_as_read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
] 
