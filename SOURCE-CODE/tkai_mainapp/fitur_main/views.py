from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseForbidden
from django.conf import settings
import base64, json, urllib3
import requests

@csrf_exempt
def requestPost(url, data):
    r = requests.post(url, data=data)
    return r.json()

def home(request, username):
    if request.method == "GET":
        tweets = requestPost(
            "{0}/timeline/find/".format(settings.API_TIMELINE),
            { "username": username }
        )
        if tweets["result"] == "success":
            tweetss = []
            for i in range(1, len(tweets)):
                tweetss.append(tweets[str(i)])
            response = {
                "tweets": tweetss
            }
            return JsonResponse({"status": 200, "data": response})
    return HttpResponseForbidden()

@csrf_exempt
def home_post(request):
    if request.method == "POST":
        data = requestPost(
            "{0}/timeline/create/".format(settings.API_TIMELINE),
            {
                "username" : request.POST["username"],
                "post" : request.POST["tweet"]
            }
        )
        return JsonResponse({"status": 200, "message": "success create timeline"})
    return HttpResponseForbidden()

@csrf_exempt
def home_delete(request):
    if request.method == "POST":
        data = requestPost(
            "{0}/timeline/delete/".format(settings.API_TIMELINE),
            {
                "username" : request.POST["username"],
                "tweet_id" : request.POST["tweet_id"]
            }
        )
        return JsonResponse({"status": 200, "message": "success delete timeline"})
    return HttpResponseForbidden()

@csrf_exempt
def login(request):
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
            return JsonResponse({"status": 200, "message": "login success"})
        return JsonResponse({"status": 200, "message": "login failed"})
    return HttpResponseForbidden()

@csrf_exempt
def signup(request):
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
            return JsonResponse({"status": 200, "message": "sign up success"})
        return JsonResponse({"status": 200, "message": "sign up failed"})
    return HttpResponseForbidden()

def profil(request, username):
    if request.method == "GET":
        dataUser = requestPost(
            "{0}/user/detail/".format(settings.API_USER),
            { "username": username }
        )
        if dataUser["result"] == "found":
            response = dataUser["data"]
            followingUser = requestPost(
                "{0}/addfriend/list-following/".format(settings.API_ADDFRIEND),
                { "username": username }
            )
            followerUser = requestPost(
                "{0}/addfriend/list-follower/".format(settings.API_ADDFRIEND),
                { "username": username }
            )
            response["follower"] = len(followerUser["data"])
            response["following"] = len(followingUser["data"])
            return JsonResponse({"status": 200, "data": response})
    return HttpResponseForbidden()

def listOfFollower(request, username):
    if request.method == "GET":
        followerUserData = requestPost(
            "{0}/addfriend/list-follower/".format(settings.API_ADDFRIEND),
            { "username": username }
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
            "username"  : username,
            "followers" : followerUser
        }
        return JsonResponse({"status": 200, "data": response})
    return HttpResponseForbidden()

def listOfFollowing(request, username):
    if request.method == "GET":
        followingUserData = requestPost(
            "{0}/addfriend/list-following/".format(settings.API_ADDFRIEND),
            { "username": username }
        )["data"]
        followingUser = [x["username"][0] for x in followingUserData]
        response = {
            "username"  : username,
            "followings" : followingUser
        }
        return JsonResponse({"status": 200, "data": response})
    return HttpResponseForbidden()

@csrf_exempt
def searchUsername(request):
    if request.method == "POST":
        username = request.POST["username"]
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
            "isFollowed"    : isFollow
        }
        return JsonResponse({"status": 200, "data": response})
    return HttpResponseForbidden()

@csrf_exempt
def unfollow(request):
    if request.method == "POST":
        data = requestPost(
            "{0}/addfriend/unfollow-person/".format(settings.API_ADDFRIEND),
            {
                "usernameX" : request.POST["username"],
                "usernameY" : request.POST["target-user"]
            }
        )
        return JsonResponse({"status": 200, "message": "success unfollow"})
    return HttpResponseForbidden()

@csrf_exempt
def follow(request):
    if request.method == "POST":
        data = requestPost(
            "{0}/addfriend/follow-person/".format(settings.API_ADDFRIEND),
            {
                "usernameX" : request.POST["username"],
                "usernameY" : request.POST["target-user"]
            }
        )
        return JsonResponse({"status": 200, "message": "success follow"})
    return HttpResponseForbidden()