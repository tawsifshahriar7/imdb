from django.shortcuts import render
from django.db import connection


def process(request):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM TV_SHOW"
        cursor.execute(sql)
        tv_shows = cursor.fetchall()
    return render(request, 'tv_show.html', {"tv_shows": tv_shows})


def detail(request, show_id):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM TV_SHOW WHERE SHOW_ID=%d" % show_id
        cursor.execute(sql)
        tv_show = cursor.fetchall()
        sql = "SELECT TR.HANDLE, TR.RATING,TR.REVIEW_TEXT from TV_SHOW T join TV_REVIEWS TR on T.SHOW_ID = TR.SHOW_ID where T.SHOW_ID=%d" % show_id
        cursor.execute(sql)
        reviews = cursor.fetchall()
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
    except KeyError:
        username = None
        loggedin = False
    user = [username, loggedin]
    return render(request, 'show_detail.html', {"tv_show": tv_show, "user": user, "reviews": reviews})
