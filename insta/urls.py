from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name='login'),
    path('signin', views.signin, name='signin'),
    path('home', views.home, name='home'),
    path('profile', views.profile, name='profile'),
]