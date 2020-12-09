from django.shortcuts import render,redirect
from django.db import connection
from django.contrib import messages


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
            messages.error(request, 'Username/Password incorrect')
            return redirect('/login/')
    return response


def register(request):
    return render(request, 'reg.html')


def registration(request):
    username = request.POST['Uname']
    password = request.POST['Pass']
    conf_password = request.POST['Pass2']
    email = request.POST['email']
    birthday = request.POST['birthday']
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
        sql = "insert into USER_IMDB(HANDLE,EMAIL,PASSWORD,BIRTHDAY) values ('%s','%s','%s',TO_DATE('%s','YYYY-MM-DD'))" % (username, email, password, birthday)
        cursor.execute(sql)
        connection.commit()
    return redirect('/login/')
