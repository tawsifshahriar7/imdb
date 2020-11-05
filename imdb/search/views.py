from django.shortcuts import render
from django.db import connection


def process(request):
    return render(request, 'search.html')


def search(request):
    text = request.POST["search_box"]
    with connection.cursor() as cursor:
        sql = "SELECT * FROM MOVIE WHERE NAME ='%s'" % text
        cursor.execute(sql)
        movies = cursor.fetchall()
        sql2 = "SELECT * FROM TV_SHOW WHERE NAME = '%s'" % text
        cursor.execute(sql2)
        shows = cursor.fetchall()
    return render(request, 'results.html',{"movies": movies, "shows": shows})
