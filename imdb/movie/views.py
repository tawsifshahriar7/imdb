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
        sql="SELECT * FROM MOVIE WHERE MOVIE_ID=%d" % movie_id
        cursor.execute(sql)
        movie_detail=cursor.fetchall()
    return render(request, 'details.html', {"movie_detail": movie_detail})

