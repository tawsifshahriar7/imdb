from django.contrib import messages
from django.shortcuts import render, redirect
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
        if cred:
            if username == cred[0][0] and password == cred[0][1]:
                loggedin = True
                is_superuser = False
                response.set_cookie('username', username)
                response.set_cookie('isLoggedIn', loggedin)
                response.set_cookie('isSuperUser', is_superuser)
            else:
                messages.error(request, 'Username/Password incorrect')
                return redirect('/login/')
        else:
            return redirect('/login/')
    return response


def register(request):
    return render(request, 'reg.html')


def registration(request):
    username = request.POST['Uname']
    password = request.POST['Pass']
    conf_password = request.POST['Pass2']
    email = request.POST['email']
    is_superuser = 'NO'
    with connection.cursor() as cursor:
        sql = "SELECT HANDLE FROM USER_IMDB WHERE HANDLE='%s'" % username
        cursor.execute(sql)
        x = cursor.fetchall()
        sql = "SELECT EMAIL FROM USER_IMDB WHERE EMAIL='%s'" % email
        cursor.execute(sql)
        y = cursor.fetchall()
        if len(x) != 0 or len(y) != 0:
            messages.error(request, 'Username/Email already exists')
            return redirect('/login/register')
        if password != conf_password:
            messages.error(request, 'passwords do not match')
            return redirect('/login/register')
        sql = "insert into USER_IMDB(HANDLE,EMAIL,PASSWORD,SUPERUSER) values ('%s','%s','%s', '%s')" % (username, email, password, is_superuser)
        cursor.execute(sql)
        connection.commit()
    return redirect('/login/')
