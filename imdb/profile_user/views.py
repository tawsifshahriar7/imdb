from django.shortcuts import render, redirect
from django.db import connection
from django.http import Http404


def process(request):
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
    except KeyError:
        username = None
        loggedin = False
        return redirect('/login/')
    user = [username, loggedin]
    return render(request, 'profile.html', {"user": user})


def logout(request):
    response = render(request, 'profile.html')
    response.delete_cookie('username')
    response.delete_cookie('isLoggedIn')
    return response


def public(request, handle):
    with connection.cursor() as cursor:
        sql = "select handle,photo from user_imdb where handle = '%s'" % handle
        cursor.execute(sql)
        profile = cursor.fetchall()
        if len(profile) == 0:
            raise Http404
    return render(request, 'public_profile.html', {"profile": profile})
