from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import datetime
import time

def getTime():
    now = datetime.datetime.now()
    return now.strftime("%d/%m/%Y, %H:%M")

# Create your views here.
@csrf_exempt
def create(request):
    response = {}
    if request.method == "POST":
        username = request.POST['username']
        text_tweet = request.POST['post']
        timestamp = getTime()
        result = insert_to_db(username, text_tweet, timestamp)
        if result is not None:
            response['result'] = "success"
            return JsonResponse(response)

    response['result'] = "failed"
    return JsonResponse(response)

@csrf_exempt
def find(request):
    response = {}
    if request.method == "POST":
        username = request.POST['username']
        result = find_db(username)
        if result is not None:
            iter_num = 1
            response['result'] = "success"
            for tweet in result:
                dict_tweet = {}
                dict_tweet['tweet_id'] = tweet[0]
                dict_tweet['username'] = tweet[1]
                dict_tweet['text'] = tweet[2]
                dict_tweet['create_time'] = tweet[3]
                dict_tweet['update_time'] = tweet[4]
                response[iter_num] = dict_tweet
                iter_num = iter_num + 1
            
            return JsonResponse(response)

    response['result'] = "failed"
    return JsonResponse(response)

@csrf_exempt
def delete(request):
    response = {}
    if request.method == "POST":
        username = request.POST['username']
        tweet_id = request.POST['tweet_id']
        result = delete_tweet_db(username, tweet_id)
        if result is not None:
            response['result'] = "success"
            response['status'] = str(tweet_id) + " has got a soft delete"
            return JsonResponse(response)

    response['result'] = "failed"
    return JsonResponse(response)

@csrf_exempt
def update(request):
    response = {}
    if request.method == "POST":
        username = request.POST['username']
        tweet_id = request.POST['tweet_id']
        text_update = request.POST['text']
        result = update_tweet_db(tweet_id, username, text_update)
        if result is not None:
            response['result'] = "success"
            response['data'] = str(tweet_id) + " has successfully updated"
            return JsonResponse(response)
    
    response['result'] = "failed"
    return JsonResponse(response)

def insert_to_db(username, text, timestamp):
    query = '''INSERT INTO tkai_2019.Tweet (username, text, create_time, flag_view)
                VALUES('{}', '{}', '{}', '1') RETURNING tweet_id '''.format(username, text, timestamp)
    result = connect_db(query, 1)
    return result

def find_db(username):
    query = '''SELECT tweet_id, username, text, create_time, update_time FROM tkai_2019.Tweet WHERE username = '{}' AND flag_view = '1' '''.format(username)
    result = connect_db(query, 0)
    return result

def delete_tweet_db(username, tweet_id):
    query = '''UPDATE tkai_2019.Tweet SET flag_view = '0' 
               WHERE tweet_id = '{}' AND username = '{}' RETURNING tweet_id'''.format(tweet_id, username)
    result = connect_db(query, 1)
    return result

def update_tweet_db(tweet_id, username, text):
    time_update = getTime()
    query = '''UPDATE tkai_2019.Tweet SET text = '{}', update_time = '{}'
               WHERE tweet_id = '{}' AND username = '{}' 
               RETURNING tweet_id'''.format(text, time_update, tweet_id, username)
    result = connect_db(query, 1)
    return result

def connect_db(query, flag):
    result = None
    with connection.cursor() as cursor:
        cursor.execute(query)
        if flag == 0:
            result = cursor.fetchall()
        else:
            result = cursor.fetchone()
    return result