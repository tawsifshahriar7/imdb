from django.shortcuts import render
from django.db import connection


def process(request):
    with connection.cursor() as cursor:
        sql="select * from movie"
        cursor.execute(sql)
        movies = cursor.fetchall()
    return render(request, 'movie.html', {"movies": movies})


def detail(request, movie_id):
    with connection.cursor() as cursor:
        sql = "SELECT MOVIE_ID, NAME, GENRE, SYNOPSIS, RELEASE_DATE, RUNTIME, LANGUAGE, POSTER,MRATING(MOVIE_ID) FROM MOVIE WHERE MOVIE_ID=%d" % movie_id
        cursor.execute(sql)
        movie_detail = cursor.fetchall()
        sql = "select MR.HANDLE,MR.RATING,MR.REVIEW_TEXT from MOVIE M join MOVIE_REVIEWS MR on M.MOVIE_ID = MR.MOVIE_ID where M.MOVIE_ID = %d" % movie_id
        cursor.execute(sql)
        movie_review = cursor.fetchall()
        sql = "select C.CELEB_ID, C.NAME from MOVIE M join MOVIE_ACTOR MA on M.MOVIE_ID = MA.MOVIE_ID join CELEB C on C.CELEB_ID = MA.CELEB_ID where M.MOVIE_ID=%d" % movie_id
        cursor.execute(sql)
        actors = cursor.fetchall()
        sql = "select C.CELEB_ID,C.NAME from MOVIE M join MOVIE_DIRECTOR MD on M.MOVIE_ID = MD.MOVIE_ID join CELEB C on C.CELEB_ID = MD.CELEB_ID where M.MOVIE_ID = %d" % movie_id
        cursor.execute(sql)
        director = cursor.fetchall()

    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
    except KeyError:
        username = None
        loggedin = False
    user = [username, loggedin]
    return render(request, 'details.html', {"movie_detail": movie_detail, "user": user, "movie_review": movie_review, "actors": actors, "director": director})

