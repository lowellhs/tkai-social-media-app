from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.conf import settings
import base64, json, urllib3
import requests

def requestPost(url, data):
    r = requests.post(url, data=data)
    return r.json()

def login(request):
    if "username" in request.session:
        return redirect("/main/home")
    return render(request, "main_login.html")

def signup(request):
    if "username" in request.session:
        return redirect("/main/home")
    return render(request, "main_signup.html")

def profil(request):
    if "username" in request.session:
        dataUser = requestPost(
            "{0}/user/detail/".format(settings.API_USER),
            { "username": request.session["username"] }
        )
        if dataUser["result"] == "found":
            response = dataUser["data"]
            followingUser = requestPost(
                "{0}/addfriend/list-following/".format(settings.API_ADDFRIEND),
                { "username": request.session["username"] }
            )
            followerUser = requestPost(
                "{0}/addfriend/list-follower/".format(settings.API_ADDFRIEND),
                { "username": request.session["username"] }
            )
            response["follower"] = len(followerUser["data"])
            response["following"] = len(followingUser["data"])
            return render(request, "main_profil.html", response)
    return redirect('/main/login')

def home(request):
    if "username" in request.session:
        tweets = requestPost(
            "{0}/timeline/find/".format(settings.API_TIMELINE),
            { "username": request.session["username"] }
        )
        if tweets["result"] == "success":
            tweetss = []
            for i in range(1, len(tweets)):
                tweetss.append(tweets[str(i)])
            response = {
                "tweets": tweetss
            }
            return render(request, "main_home.html", response)
    return redirect('/main/login')

def listOfFollower(request):
    if "username" in request.session:
        followerUserData = requestPost(
            "{0}/addfriend/list-follower/".format(settings.API_ADDFRIEND),
            { "username": request.session["username"] }
        )["data"]
        followerUser = []
        for x in followerUserData:
            followerUser.append(
                {
                    "username": x["username"][0],
                    "relate": x["isfollow"]
                }
            )
        response = {
            "username"  : "username", #get from session
            "followers" : followerUser
        }
        return render(request, "main_listOfFollower.html", response)
    return redirect('/main/login')

def listOfFollowing(request):
    if "username" in request.session:
        followingUserData = requestPost(
            "{0}/addfriend/list-following/".format(settings.API_ADDFRIEND),
            { "username": request.session["username"] }
        )["data"]
        followingUser = [x["username"][0] for x in followingUserData]
        response = {
            "username"  : request.session["username"],
            "followings" : followingUser
        }
        print(response)
        return render(request, "main_listOfFollowing.html", response)
    return redirect('/main/login')

def searchUsername(request):
    if "username" in request.session:
        response = {
            "isPost"  : False
        }
        if request.method == "POST":
            username = request.session["username"]
            searchUser = request.POST["search"]
            data = requestPost(
                "{0}/user/detail/".format(settings.API_USER),
                {"username": searchUser}
            )
            userFound = False
            if data["result"] == "found" and username != searchUser:
                userFound = True

            isFollow = requestPost(
                "{0}/addfriend/is-follow/".format(settings.API_ADDFRIEND),
                {
                    "usernameX": username,
                    "usernameY": searchUser
                }
            )["isfollow"]

            response = {
                "foundUsername" : searchUser,
                "userFound"     : userFound,
                "isPost"        : True,
                "isFollowed"    : isFollow
            }
        return render(request, "main_searchUsername.html", response)
    return redirect('/main/login')

def login_post(request):
    if request.method == "POST":
        fields = {
            "username": request.POST["username"], 
            "password": request.POST["password"]
        }
        data = requestPost(
            "{0}/user/login/".format(settings.API_USER),
            fields
        )
        if data["result"]:
            request.session["username"] = fields["username"]
            return redirect("/main/home/")
    return redirect("/main/login/")

def signup_post(request):
    if request.method == "POST":
        fields = {
            "username"      : request.POST['username'], 
            "password"      : request.POST['password'],
            "fullname"      : request.POST['fullname'],
            "email"         : request.POST['email'],
            "profile_pict"  : request.POST['profile-pict']
        }
        data = requestPost(
            "{0}/user/regis/".format(settings.API_USER),
            fields
        )
        if data["result"] == "success":
            return redirect("/main/login")
    return redirect("/main/signup")

def home_post(request):
    if request.method == "POST":
        data = requestPost(
            "{0}/timeline/create/".format(settings.API_TIMELINE),
            {
                "username" : request.session["username"],
                "post" : request.POST["tweet"]
            }
        )
    return redirect("/main/home")

def home_delete(request):
    if request.method == "POST":
        data = requestPost(
            "{0}/timeline/delete/".format(settings.API_TIMELINE),
            {
                "username" : request.session["username"],
                "tweet_id" : request.POST["tweet_id"]
            }
        )
    return redirect("/main/home")

def logout(request):
    if request.method == "POST":
        request.session.pop("username")
        return redirect('/main/login')
    return redirect('/main/home')

def unfollow(request):
    if request.method == "POST":
        data = requestPost(
            "{0}/addfriend/unfollow-person/".format(settings.API_ADDFRIEND),
            {
                "usernameX" : request.session["username"],
                "usernameY" : request.POST["target-user"]
            }
        )
        return redirect(request.POST["target-url"])
    return redirect("/main/search/")

def follow(request):
    if request.method == "POST":
        data = requestPost(
            "{0}/addfriend/follow-person/".format(settings.API_ADDFRIEND),
            {
                "usernameX" : request.session["username"],
                "usernameY" : request.POST["target-user"]
            }
        )
        return redirect(request.POST["target-url"])
    return redirect("/main/search/")