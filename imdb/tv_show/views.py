from django.shortcuts import render,redirect
from django.db import connection


def process(request):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM TV_SHOW"
        cursor.execute(sql)
        tv_shows = cursor.fetchall()
    return render(request, 'tv_show.html', {"tv_shows": tv_shows})


def detail(request, show_id):
    with connection.cursor() as cursor:
        sql = "SELECT SHOW_ID, NAME, GENRE, SYNOPSIS, RELEASE_DATE, LANGUAGE, POSTER,TRATING(SHOW_ID) FROM TV_SHOW WHERE SHOW_ID=%d" % show_id
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


def submit_review(request, show_id):
    rating = int(request.POST['rating'])
    review_text = request.POST['review_text']
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
    except KeyError:
        return redirect('/login/')
    with connection.cursor() as cursor:
        sql = "SELECT * FROM TV_REVIEWS WHERE HANDLE='%s' AND SHOW_ID=%d" % (username, show_id)
        cursor.execute(sql)
        previous_review = cursor.fetchall()
        if len(previous_review) == 0:
            sql = "INSERT INTO TV_REVIEWS VALUES(%d,'%s',%d,'%s')" % (show_id, username, rating, review_text)
        else:
            sql = "UPDATE TV_REVIEWS SET RATING=%d,REVIEW_TEXT='%s' WHERE SHOW_ID=%d" % (rating, review_text, show_id)
        cursor.execute(sql)
        connection.commit()
    return redirect('/tvshow/%d/' % show_id)
