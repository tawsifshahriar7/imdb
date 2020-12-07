from django.shortcuts import render,redirect
from django.db import connection
import re


def process(request):
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
    except KeyError:
        username = None
        loggedin = False
    if username == 'admin':
        user = [username, loggedin]
        return render(request, 'superuser.html', {"user": user})
    else:
        return redirect('/login/')


def add_movie(request):
    return render(request, 'new_movie_form.html')


def add_tvshow(request):
    return render(request, 'new_tvshow_form.html')


def add_episode(request):
    return render(request, 'new_episode_form.html')


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
    cast = request.POST['cast']
    director = request.POST['director']
    producer = request.POST['producer']
    writer = request.POST['writer']
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
            movie_cast(cast, movie_id)
            movie_director(director, movie_id)
            movie_producer(producer, movie_id)
            movie_writer(writer, movie_id)
    return redirect('/superuser/')


def movie_cast(cast, movie_id):
    cast_list = re.findall(r'\d+', cast)
    for actor in cast_list:
        with connection.cursor() as cursor:
            sql = "INSERT INTO MOVIE_ACTOR VALUES(%d,%d)" % (movie_id, int(actor))
            cursor.execute(sql)
            connection.commit()


def movie_director(director, movie_id):
    director_list = re.findall(r'\d+', director)
    for director in director_list:
        with connection.cursor() as cursor:
            sql = "INSERT INTO MOVIE_DIRECTOR VALUES(%d,%d)" % (movie_id, int(director))
            cursor.execute(sql)
            connection.commit()


def movie_producer(producer, movie_id):
    producer_list = re.findall(r'\d+', producer)
    for producer in producer_list:
        with connection.cursor() as cursor:
            sql = "INSERT INTO MOVIE_PRODUCER VALUES(%d,%d)" % (movie_id, int(producer))
            cursor.execute(sql)
            connection.commit()


def movie_writer(writer, movie_id):
    writer_list = re.findall(r'\d+', writer)
    for writer in writer_list:
        with connection.cursor() as cursor:
            sql = "INSERT INTO MOVIE_WRITER VALUES(%d,%d)" % (movie_id, int(writer))
            cursor.execute(sql)
            connection.commit()


def show_added(request):
    name = request.POST['show_name']
    genre = request.POST['genre']
    synopsis = request.POST['synopsis']
    poster = request.POST['poster']
    release_date = request.POST['release_date']
    language = request.POST['language']
    producer = request.POST['producer']
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
            tvshow_producer(producer, show_id)
    return redirect('/superuser/')


def tvshow_producer(producer, show_id):
    producer_list = re.findall(r'\d+', producer)
    for producer in producer_list:
        with connection.cursor() as cursor:
            sql = "INSERT INTO TV_PRODUCER VALUES(%d,%d)" % (show_id, int(producer))
            cursor.execute(sql)
            connection.commit()


def celeb_added(request):
        name = request.POST['name']
        photo = request.POST['photo']
        biography = request.POST['biography']
        height = request.POST['height']
        if len(height) != 0:
            height = float(height)
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


def episode_added(request):
    show_id = int(request.POST['show_id'])
    season_no = int(request.POST['season_no'])
    episode_no = int(request.POST['episode_no'])
    name = request.POST['episode_name']
    synopsis = request.POST['synopsis']
    release_date = request.POST['release_date']
    runtime = int(request.POST['runtime'])
    poster = request.POST['poster']
    cast = request.POST['cast']
    director = request.POST['director']
    writer = request.POST['writer']
    with connection.cursor() as cursor:
        sql = "SELECT SHOW_ID FROM EPISODE WHERE SHOW_ID=%d AND SEASON_NO=%d AND EPISODE_NO=%d" % (show_id, season_no, episode_no)
        cursor.execute(sql)
        x = cursor.fetchall()
        if len(x) == 0:
            sql = "INSERT INTO EPISODE VALUES(%d,%d,%d,'%s','%s',TO_DATE('%s','YYYY-MM-DD'),%d,'%s')" % (show_id, season_no, episode_no, name, synopsis, release_date, runtime, poster)
            cursor.execute(sql)
            connection.commit()
            episode_cast(cast, show_id, season_no, episode_no)
            episode_director(director, show_id, season_no, episode_no)
            episode_writer(writer, show_id, season_no, episode_no)
    return redirect('/superuser/')


def episode_cast(cast, show_id, season_no, episode_no):
    cast_list = re.findall(r'\d+', cast)
    for actor in cast_list:
        with connection.cursor() as cursor:
            sql = "INSERT INTO EPISODE_ACTOR VALUES(%d,%d,%d,%d)" % (show_id, season_no, episode_no, int(actor))
            cursor.execute(sql)
            connection.commit()


def episode_director(director, show_id, season_no, episode_no):
    director_list = re.findall(r'\d+', director)
    for director in director_list:
        with connection.cursor() as cursor:
            sql = "INSERT INTO EPISODE_DIRECTOR VALUES(%d,%d,%d,%d)" % (show_id, season_no, episode_no, int(director))
            cursor.execute(sql)
            connection.commit()


def episode_writer(writer, show_id, season_no, episode_no):
    writer_list = re.findall(r'\d+', writer)
    for writer in writer_list:
        with connection.cursor() as cursor:
            sql = "INSERT INTO EPISODE_WRITER VALUES(%d,%d,%d,%d)" % (show_id, season_no, episode_no, int(writer))
            cursor.execute(sql)
            connection.commit()
