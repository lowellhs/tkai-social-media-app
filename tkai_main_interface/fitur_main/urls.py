from django.urls import path
from .views import *

urlpatterns = [
    path('home/', home, name="home"),
    path('login/', login, name="login"),
    path('signup/', signup, name="signup"),
    path('profile/', profil, name="profile"),
    path('follower/', listOfFollower, name="follower"),
    path('following/', listOfFollowing, name="following"),
    path('search/', searchUsername, name="search"),
    path('login-post/', login_post, name="login-post"),
    path('signup-post/', signup_post, name="signup-post"),
    path('home-post/', home_post, name="home-post"),
    path('home-delete/', home_delete, name="home-delete"),
    path('logout/', logout, name="logout"),
    path('unfollow/', unfollow, name="unfollow"),
    path('follow/', follow, name="follow"),
]
