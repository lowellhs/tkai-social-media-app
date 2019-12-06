from django.http import JsonResponse
import psycopg2, hashlib, binascii, os
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

@csrf_exempt
def follow_person(request):
    if request.method == "POST":
        usernameX = request.POST["usernameX"]
        usernameY = request.POST["usernameY"]
        insert_to_db_following_or_follower(usernameX, usernameY)
        return JsonResponse({"message":"success"})
    return JsonResponse({"message":"invalid method"})

@csrf_exempt
def unfollow_person(request):
    if request.method == "POST":
        usernameX = request.POST["usernameX"]
        usernameY = request.POST["usernameY"]
        delete_to_db_following_or_follower(usernameX, usernameY)
        return JsonResponse({"message":"success"})
    return JsonResponse({"message":"invalid method"})

@csrf_exempt
def list_follower(request):
    response = {"data":[]}
    if request.method == "POST":
        username = request.POST["username"]
        follower = find_db_follower(username)
        if follower is not None:
            for person in follower:
                response["data"].append({"username":person,"isfollow":is_follow_person(username,person[0])})
    return JsonResponse(response)

@csrf_exempt
def list_following(request):
    response = {"data":[]}
    if request.method == "POST":
        username = request.POST["username"]
        following = find_db_following(username)
        if following is not None:
            for person in following:
                response["data"].append({"username":person})
    return JsonResponse(response)

@csrf_exempt
def is_follow_person_API(request):
    if request.method == "POST":
        usernameX = request.POST['usernameX']
        usernameY = request.POST['usernameY']
        if (is_follow_person(usernameX, usernameY)):
            return JsonResponse({"isfollow":True})
        return JsonResponse({"isfollow":False})
    return JsonResponse({"message":"invalid"})

        
def is_follow_person(usernameX,usernameY):
    query = "SELECT * FROM tkai_2019.follow WHERE usernameX = '{}' and usernameY = '{}'".format(usernameX, usernameY)
    result = connect_db(query, 0)
    if (result):
        return True
    return False

def find_db_follower(username):
    query = "SELECT usernameX FROM tkai_2019.follow WHERE usernameY = '{}'".format(username)
    result = connect_db(query, 0)
    return result

def find_db_following(username):
    query = "SELECT usernameY FROM tkai_2019.follow WHERE usernameX = '{}'".format(username)
    result = connect_db(query, 0)
    return result

def delete_to_db_following_or_follower(usernameX, usernameY):
    try:
        query = '''DELETE FROM tkai_2019."follow" WHERE usernameX = '{}' and usernameY = '{}'
                    RETURNING usernameX,usernameY'''.format(usernameX,usernameY)
        connect_db(query, 1)
        return True, "Success"
    except:
        return False, "Error"    

def insert_to_db_following_or_follower(usernameX, usernameY):
    try:
        query = '''INSERT INTO tkai_2019."follow"(usernameX,usernameY) VALUES('{}','{}') 
                    RETURNING usernameX,usernameY'''.format(usernameX,usernameY)
        connect_db(query, 1)
        return True, "Success"
    except:
        return False, "Error"

def connect_db(query, flag):
    result = None
    with connection.cursor() as cursor:
        cursor.execute(query)
        if flag == 0:
            result = cursor.fetchall()
        else:
            result = cursor.fetchone()
    return result