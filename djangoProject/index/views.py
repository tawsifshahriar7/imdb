from django.shortcuts import render
from django.db import connection


def process(request):
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
        is_superuser = request.COOKIES['isSuperUser']
    except KeyError:
        username = None
        loggedin = False
        is_superuser = False
    user = [username, loggedin, is_superuser]
    with connection.cursor() as cursor:
        sql = "SELECT * FROM NEW_MOVIE ORDER BY TIME DESC"
        cursor.execute(sql)
        new_movies = cursor.fetchall()
        sql = "SELECT * FROM NEW_SHOW ORDER BY TIME DESC"
        cursor.execute(sql)
        new_shows = cursor.fetchall()
    return render(request, 'index.html', {"user": user, "new_movies": new_movies, "new_shows": new_shows})

