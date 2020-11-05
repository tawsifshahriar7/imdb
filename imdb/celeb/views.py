from django.shortcuts import render
from django.db import connection


def process(request):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM CELEB"
        cursor.execute(sql)
        celebs = cursor.fetchall()
    return render(request, 'celeb.html', {"celebs": celebs})


def detail(request, celeb_id):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM CELEB WHERE CELEB_ID=%d" % celeb_id
        cursor.execute(sql)
        celeb = cursor.fetchall()
    return render(request, 'detail.html', {"celeb": celeb})
