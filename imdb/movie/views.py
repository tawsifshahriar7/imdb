from django.shortcuts import render,redirect
from django.db import connection


def process(request):
    with connection.cursor() as cursor:
        sql="select * from movie"
        cursor.execute(sql)
        movies = cursor.fetchall()
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
    except KeyError:
        username = None
        loggedin = False
    user = [username,loggedin]
    return render(request, 'movie.html', {"movies": movies, "user": user})


def detail(request, movie_id):
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
    except KeyError:
        username = None
        loggedin = False
    user = [username, loggedin]
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
        sql = "SELECT STATUS FROM MOVIE_WATCHLIST WHERE MOVIE_ID=%d AND HANDLE='%s'" % (movie_id, username)
        cursor.execute(sql)
        status = cursor.fetchall()
        if len(status) == 0:
            status = False
        elif status[0][0] == 'True':
            status = True
        else:
            status = False

    return render(request, 'details.html', {"movie_detail": movie_detail, "user": user, "movie_review": movie_review, "actors": actors, "director": director, "status": status})


def submit_review(request, movie_id):
    rating = int(request.POST['rating'])
    review_text = request.POST['review_text']
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
    except KeyError:
        return redirect('/login/')
    with connection.cursor() as cursor:
        sql = "SELECT * FROM MOVIE_REVIEWS WHERE HANDLE='%s' AND MOVIE_ID=%d" % (username, movie_id)
        cursor.execute(sql)
        previous_review = cursor.fetchall()
        if len(previous_review) == 0:
            sql = "INSERT INTO MOVIE_REVIEWS VALUES(%d,'%s',%d,'%s')" % (movie_id, username, rating, review_text)
        else:
            sql = "UPDATE MOVIE_REVIEWS SET RATING=%d,REVIEW_TEXT='%s' WHERE MOVIE_ID=%d" % (rating, review_text, movie_id)
        cursor.execute(sql)
        connection.commit()
    return redirect('/movie/%d/' % movie_id)


def add_to_watchlist(request, movie_id):
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
    except KeyError:
        username = None
        loggedin = False
    if not loggedin:
        return redirect('/movie/%d/' % movie_id)
    with connection.cursor() as cursor:
        sql = "SELECT STATUS FROM MOVIE_WATCHLIST WHERE MOVIE_ID=%d AND HANDLE='%s'" % (movie_id, username)
        cursor.execute(sql)
        status = cursor.fetchall()
        if len(status) == 0:
            sql = "INSERT INTO MOVIE_WATCHLIST VALUES(%d,'%s','True')" % (movie_id, username)
        else:
            sql = "UPDATE MOVIE_WATCHLIST SET STATUS='True' WHERE MOVIE_ID=%d AND HANDLE='%s'" % (movie_id, username)
        cursor.execute(sql)
        connection.commit()
    return redirect('/movie/%d' % movie_id)


def remove_from_watchlist(request, movie_id):
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
    except KeyError:
        username = None
        loggedin = False
    if not loggedin:
        return redirect('/movie/%d/' % movie_id)
    with connection.cursor() as cursor:
        sql = "UPDATE MOVIE_WATCHLIST SET STATUS='False' WHERE MOVIE_ID=%d AND HANDLE='%s'" % (movie_id, username)
        cursor.execute(sql)
        connection.commit()
    return redirect('/movie/%d' % movie_id)
