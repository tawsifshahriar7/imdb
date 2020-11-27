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
        user = [username,loggedin]
        return render(request, 'superuser.html', {"user": user})
    else:
        return redirect('/login/')


def add_movie(request):
    return render(request, 'new_movie_form.html')


def add_tvshow(request):
    return render(request, 'new_tvshow_form.html')


def add_celeb(request):
    return render(request,'new_celeb_form.html')


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


def show_added(request):
    name = request.POST['show_name']
    genre = request.POST['genre']
    synopsis = request.POST['synopsis']
    poster = request.POST['poster']
    release_date = request.POST['release_date']
    language = request.POST['language']
    with connection.cursor() as cursor:
        sql = "SELECT NAME FROM TV_SHOW WHERE NAME='%s'" % name
        cursor.execute(sql)
        x = cursor.fetchall()
        if len(x) == 0:
            sql = "SELECT MAX(SHOW_ID) FROM TV_SHOW"
            cursor.execute(sql)
            id = cursor.fetchall()
            show_id = int(id[0][0])
            show_id = show_id + 1
            sql = "INSERT INTO TV_SHOW VALUES(%d,'%s','%s','%s',TO_DATE('%s','YYYY-MM-DD'),'%s','%s')" % (show_id, name, genre, synopsis, release_date, language, poster)
            cursor.execute(sql)
            connection.commit()
    return redirect('/superuser/')


def celeb_added(request):
        name = request.POST['name']
        photo = request.POST['photo']
        biography = request.POST['biography']
        height = float(request.POST['height'])
        birthday = request.POST['birthday']
        deathday = request.POST['deathday']
        with connection.cursor() as cursor:
            sql = "SELECT NAME FROM CELEB WHERE NAME='%s'" % name
            cursor.execute(sql)
            x = cursor.fetchall()
            if len(x) == 0:
                sql = "SELECT MAX(CELEB_ID) FROM CELEB"
                cursor.execute(sql)
                id = cursor.fetchall()
                celeb_id = int(id[0][0])
                celeb_id = celeb_id + 1
                sql = "INSERT INTO CELEB VALUES(%d,'%s','%s',TO_DATE('%s','YYYY-MM-DD'),TO_DATE('%s','YYYY-MM-DD'),'%s','%s')" % (celeb_id, name, photo, birthday, deathday, biography, height)
                cursor.execute(sql)
                connection.commit()
        return redirect('/superuser/')
