from django.shortcuts import render, redirect
from django.db import connection
from django.http import Http404,HttpResponseRedirect


def process(request):
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
    except KeyError:
        username = None
        loggedin = False
        return redirect('/login/')
    user = [username, loggedin]
    with connection.cursor() as cursor:
        sql = "select RATING,M2.NAME from MOVIE_REVIEWS M join MOVIE M2 on M2.MOVIE_ID = M.MOVIE_ID where HANDLE='%s' UNION SELECT RATING,TS.NAME from TV_REVIEWS join TV_SHOW TS on TS.SHOW_ID = TV_REVIEWS.SHOW_ID where HANDLE='%s'" % (username, username)
        cursor.execute(sql)
        rating = cursor.fetchall()
        sql = "select REVIEW_TEXT,M2.NAME from MOVIE_REVIEWS M join MOVIE M2 on M2.MOVIE_ID = M.MOVIE_ID where HANDLE='%s' UNION SELECT REVIEW_TEXT,TS.NAME from TV_REVIEWS join TV_SHOW TS on TS.SHOW_ID = TV_REVIEWS.SHOW_ID where HANDLE='%s'" % (username, username)
        cursor.execute(sql)
        review = cursor.fetchall()
        sql = "select MW.HANDLE,MW.MOVIE_ID,M.NAME from MOVIE_WATCHLIST MW join MOVIE M on M.MOVIE_ID = MW.MOVIE_ID where MW.HANDLE='%s' and MW.STATUS='True'" % username
        cursor.execute(sql)
        movie_watchlist = cursor.fetchall()
        sql = "select TW.HANDLE,TW.SHOW_ID,T.NAME from TV_SHOW_WATCHLIST TW join TV_SHOW T on T.SHOW_ID = TW.SHOW_ID where TW.HANDLE='%s' and TW.STATUS='True'" % username
        cursor.execute(sql)
        show_watchlist = cursor.fetchall()
        watchlist = [movie_watchlist, show_watchlist]
    return render(request, 'profile.html', {"user": user, "rating": rating, "review": review, "watchlist": watchlist})


def logout(request):
    response = redirect('/')
    response.delete_cookie('username')
    response.delete_cookie('isLoggedIn')
    return response


def public(request, handle):
    with connection.cursor() as cursor:
        sql = "select handle,photo from user_imdb where handle = '%s'" % handle
        cursor.execute(sql)
        profile = cursor.fetchall()
        if len(profile) == 0:
            raise Http404
    return render(request, 'public_profile.html', {"profile": profile})
