from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import hashlib, binascii, os

# Create your views here.
@csrf_exempt
def login(request):
    response = {}
    username = request.POST['username']
    password = request.POST['password']
    if request.method == "POST":
        username = validate_user(username)
        if username is not None:
            password = validate_pass(password, username[0])
            if password:
                response['result'] = True
                return JsonResponse(response)
    response["result"] = False 
    return JsonResponse(response)

@csrf_exempt
def regis(request):
    response = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        fullname = request.POST['fullname']
        email = request.POST['email']
        profile_pict = request.POST['profile_pict']
        user = validate_user(username)
        if user is None:
            username = insert_to_db(username, password, fullname, email, profile_pict)
            if username is not None:
                response['result'] = "success"
                return JsonResponse(response)

    response['result'] = "failed"
    return JsonResponse(response)

@csrf_exempt
def get_detail_user(request):
    response = {}
    if request.method == "POST":
        detail_data = get_detail_user_db(request.POST['username'])
        if detail_data is not None:
            response['result'] = "found"
            response['data'] = {'username': detail_data[0], 'fullname': detail_data[1],
                                    'email': detail_data[2], 'profile_pict': detail_data[3]}
            return JsonResponse(response)

    response['result'] = "not found"
    return JsonResponse(response)

@csrf_exempt
def update_profile(request):
    response = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        fullname = request.POST['fullname']
        email = request.POST['email']
        profile_pict = request.POST['profile_pict']
        result = update_profile_db(username, password, fullname, email, profile_pict)
        if result is not None:
            response['result'] = "success"
            return JsonResponse(response)

    response['result'] = "not update"
    return JsonResponse(response)

def get_detail_user_db(username):
    query = '''SELECT username, fullname, email, profile_pict FROM tkai_2019.Pengguna
                WHERE username = '{}' '''.format(username)
    result = connect_db(query, "0")
    return result

def update_profile_db(username, password, fullname, email, profile_pict):
    cek = False
    query = '''UPDATE tkai_2019.Pengguna SET '''
    query_update = ""
    if username is not None:
        query_update = query_update + "username = '{}', ".format(username)
        cek = True
    if password is not None:
        pwdhash = hash_pass(password)
        query_update = query_update + "password = '{}'".format(pwdhash)
        cek = True
    if fullname is not None:
        query_update = query_update + "fullname = '{}'".format(fullname)
        cek = True
    if email is not None:
        query_update = query_update + "email = '{}'".format(email)
        cek = True
    if profile_pict is not None:
        query_update = query_update + "profile_pict = '{}'".format(profile_pict)
        cek = True
    
    if cek:
        query_update = query_update.rstrip(',')
        query = query + query_update + " WHERE username = '{}' RETURNING username".format(username)
        result = connect_db(query, "0")
        return result

    return None

def validate_user(username):
    query = '''SELECT password FROM tkai_2019.Pengguna
               WHERE username = '{}'
                 '''.format(username)
    result = connect_db(query, "0")
    return result

def validate_pass(inputpass, realpass):
    salt = realpass[:64]
    realpass = realpass[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', inputpass.encode('utf-8'),
                                  salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return realpass == pwdhash
    
def hash_pass(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def insert_to_db(username, password, fullname, email, profile_pict):
    hashpwd = hash_pass(password)
    query = '''INSERT INTO tkai_2019.Pengguna(username, password, fullname, email, profile_pict)
                VALUES('{}', '{}', '{}', '{}', '{}')
                RETURNING username'''.format(username, hashpwd, fullname, email, profile_pict)

    result = connect_db(query, "0")
    return result

def connect_db(query, flag):
    result = None
    with connection.cursor() as cursor:
        cursor.execute(query)
        if flag == "0":
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()
    return result