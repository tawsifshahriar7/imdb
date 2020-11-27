from django.shortcuts import render,redirect
from django.db import connection


def process(request):
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
    except KeyError:
        username = None
        loggedin = False
    if username == 'admin':
        return render(request, 'superuser.html')
    else:
        return redirect('/login/')


def add_movie(request):
    return render(request, 'new_movie_form.html')


def movie_added(request):
    name = request.POST['movie_name']
    genre = request.POST['genre']
    synopsis = request.POST['synopsis']
    poster = request.POST['poster']
    release_date = request.POST['release_date']
    runtime = request.POST['runtime']
    runtime = int(runtime)
    language = request.POST['language']
    with connection.cursor() as cursor:
        sql = "SELECT NAME FROM MOVIE WHERE NAME='%s'" % name
        cursor.execute(sql)
        x = cursor.fetchall()
        if len(x) == 0:
            sql = "SELECT MAX(MOVIE_ID) FROM MOVIE"
            cursor.execute(sql)
            id = cursor.fetchall()
            movie_id = int(id[0][0])
            movie_id = movie_id+1
            sql = "INSERT INTO MOVIE VALUES(%d,'%s','%s','%s',TO_DATE('%s','YYYY-MM-DD'),%d,'%s','%s')" % (movie_id, name, genre, synopsis, release_date, runtime, language, poster)
            cursor.execute(sql)
            connection.commit()
    return redirect('/superuser/')
