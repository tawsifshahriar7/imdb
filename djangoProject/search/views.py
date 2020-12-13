from django.shortcuts import render
from django.db import connection


def process(request):
    return render(request, 'search.html')


def search(request):
    text = request.POST["search_box"]
    if bool(text):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM MOVIE WHERE UPPER(NAME) LIKE UPPER('%%%s%%')" % text
            cursor.execute(sql)
            movies = cursor.fetchall()
            sql2 = "SELECT * FROM TV_SHOW WHERE UPPER(NAME) LIKE UPPER('%%%s%%')" % text
            cursor.execute(sql2)
            shows = cursor.fetchall()
            sql3 = "SELECT * FROM CELEB WHERE UPPER(NAME) LIKE UPPER('%%%s%%')" % text
            cursor.execute(sql3)
            celebs = cursor.fetchall()
        try:
            username = request.COOKIES['username']
            loggedin = request.COOKIES['isLoggedIn']
            is_superuser = request.COOKIES['isSuperUser']
        except KeyError:
            username = None
            loggedin = False
            is_superuser = False
        user = [username, loggedin, is_superuser]
        return render(request, 'results.html', {"movies": movies, "shows": shows, "celebs": celebs, "user": user})
    else:
        return render(request, 'results.html')

