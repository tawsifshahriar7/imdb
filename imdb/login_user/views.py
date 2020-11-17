from django.shortcuts import render,redirect
from django.db import connection


def process(request):
    return render(request, 'login_user.html')


def login(request):
    username = request.POST["Uname"]
    password = request.POST["Pass"]
    with connection.cursor() as cursor:
        sql = "SELECT HANDLE,PASSWORD FROM USER_IMDB WHERE HANDLE='%s'" % username
        cursor.execute(sql)
        cred = cursor.fetchall()
        response = redirect('/')
        if username == cred[0][0] and password == cred[0][1]:
            loggedin = True
            response.set_cookie('username', username)
            response.set_cookie('isLoggedIn', loggedin)
        else:
            return redirect('/login/')
    return response


def register(request):
    return render(request, 'reg.html')

