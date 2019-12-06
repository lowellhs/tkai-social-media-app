from django.urls import path
from .views import *

urlpatterns = [
    path('home-detail/<str:username>/', home, name="home-detail"),
    path('home-post/', home_post, name="home-post"),
    path('home-delete/', home_delete, name="home-delete"),
    path('login/', login, name="login"),
    path('signup/', signup, name="signup"),
    path('profile/<str:username>/', profil, name="profile"),
    path('follower/<str:username>/', listOfFollower, name="follower"),
    path('following/<str:username>/', listOfFollowing, name="following"),
    path('search/', searchUsername, name="search"),
    path('unfollow/', unfollow, name="unfollow"),
    path('follow/', follow, name="follow"),
]
