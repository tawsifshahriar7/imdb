from django.shortcuts import render,redirect
from django.db import connection


def process(request):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM TV_SHOW"
        cursor.execute(sql)
        tv_shows = cursor.fetchall()
    return render(request, 'tv_show.html', {"tv_shows": tv_shows})


def detail(request, show_id):
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
    except KeyError:
        username = None
        loggedin = False
    user = [username, loggedin]
    with connection.cursor() as cursor:
        sql = "SELECT SHOW_ID, NAME, GENRE, SYNOPSIS, RELEASE_DATE, LANGUAGE, POSTER,TRATING(SHOW_ID) FROM TV_SHOW WHERE SHOW_ID=%d" % show_id
        cursor.execute(sql)
        tv_show = cursor.fetchall()
        sql = "SELECT TR.HANDLE, TR.RATING,TR.REVIEW_TEXT from TV_SHOW T join TV_REVIEWS TR on T.SHOW_ID = TR.SHOW_ID where T.SHOW_ID=%d" % show_id
        cursor.execute(sql)
        reviews = cursor.fetchall()
        sql = "SELECT STATUS FROM TV_SHOW_WATCHLIST WHERE SHOW_ID=%d AND HANDLE='%s'" % (show_id, username)
        cursor.execute(sql)
        status = cursor.fetchall()
        if len(status) == 0:
            status = False
        elif status[0][0] == 'True':
            status = True
        else:
            status = False
    return render(request, 'show_detail.html', {"tv_show": tv_show, "user": user, "reviews": reviews, "status": status})


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


def add_to_watchlist(request, show_id):
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
    except KeyError:
        username = None
        loggedin = False
    if not loggedin:
        return redirect('/tvshow/%d/' % show_id)
    with connection.cursor() as cursor:
        sql = "SELECT STATUS FROM TV_SHOW_WATCHLIST WHERE SHOW_ID=%d AND HANDLE='%s'" % (show_id, username)
        cursor.execute(sql)
        status = cursor.fetchall()
        if len(status) == 0:
            sql = "INSERT INTO TV_SHOW_WATCHLIST VALUES(%d,'%s','True')" % (show_id, username)
        else:
            sql = "UPDATE TV_SHOW_WATCHLIST SET STATUS='True' WHERE SHOW_ID=%d AND HANDLE='%s'" % (show_id, username)
        cursor.execute(sql)
        connection.commit()
    return redirect('/tvshow/%d' % show_id)


def remove_from_watchlist(request, show_id):
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
    except KeyError:
        username = None
        loggedin = False
    if not loggedin:
        return redirect('/tvshow/%d/' % show_id)
    with connection.cursor() as cursor:
        sql = "UPDATE TV_SHOW_WATCHLIST SET STATUS='False' WHERE SHOW_ID=%d AND HANDLE='%s'" % (show_id, username)
        cursor.execute(sql)
        connection.commit()
    return redirect('/tvshow/%d' % show_id)


def episode_details(request, show_id, season_no, episode_no):
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
    except KeyError:
        username = None
        loggedin = False
    user = [username, loggedin]
    with connection.cursor() as cursor:
        sql = "SELECT * FROM EPISODE WHERE SHOW_ID=%d AND SEASON_NO=%d AND EPISODE_NO=%d" % (show_id, season_no, episode_no)
        cursor.execute(sql)
        episode = cursor.fetchall()
        sql = "select ER.HANDLE,ER.RATING,ER.REVIEW_TEXT from EPISODE_REVIEWS ER join EPISODE E on E.SHOW_ID = ER.SHOW_ID and E.SEASON_NO = ER.SEASON_NO and E.EPISODE_NO = ER.EPISODE_NO where E.SHOW_ID=%d AND E.SEASON_NO=%d AND E.EPISODE_NO=%d" % (show_id, season_no, episode_no)
        cursor.execute(sql)
        reviews = cursor.fetchall()
        sql = "select C.CELEB_ID,C.NAME from EPISODE_ACTOR EA join CELEB C on C.CELEB_ID = EA.CELEB_ID where EA.SHOW_ID=%d and EA.SEASON_NO=%d and EA.EPISODE_NO=%d" % (show_id, season_no, episode_no)
        cursor.execute(sql)
        actors = cursor.fetchall()
        sql = "select C.CELEB_ID,C.NAME from EPISODE_DIRECTOR ED join CELEB C on C.CELEB_ID = ED.CELEB_ID where ED.SHOW_ID=%d and ED.SEASON_NO=%d and ED.EPISODE_NO=%d" % (show_id, season_no, episode_no)
        cursor.execute(sql)
        directors = cursor.fetchall()
        sql = "select C.CELEB_ID,C.NAME from EPISODE_WRITER EW join CELEB C on C.CELEB_ID = EW.CELEB_ID where EW.SHOW_ID=%d and EW.SEASON_NO=%d and EW.EPISODE_NO=%d" % (show_id, season_no, episode_no)
        cursor.execute(sql)
        writers = cursor.fetchall()
    return render(request, 'episode_details.html', {"episode": episode, "user": user, "reviews": reviews, "actors": actors, "directors": directors, "writers": writers})


def episode_submit_review(request, show_id, season_no, episode_no):
    rating = int(request.POST['rating'])
    review_text = request.POST['review_text']
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
    except KeyError:
        return redirect('/login/')
    with connection.cursor() as cursor:
        sql = "SELECT * FROM EPISODE_REVIEWS WHERE HANDLE='%s' AND SHOW_ID=%d AND SEASON_NO=%d AND EPISODE_NO=%d" % (username, show_id, season_no, episode_no)
        cursor.execute(sql)
        previous_review = cursor.fetchall()
        if len(previous_review) == 0:
            sql = "INSERT INTO EPISODE_REVIEWS VALUES(%d,%d,%d,'%s',%d,'%s')" % (show_id, season_no, episode_no, username, rating, review_text)
        else:
            sql = "UPDATE EPISODE_REVIEWS SET RATING=%d,REVIEW_TEXT='%s' WHERE SHOW_ID=%d AND SEASON_NO=%d AND EPISODE_NO=%d" % (rating, review_text, show_id, season_no, episode_no)
        cursor.execute(sql)
        connection.commit()
    return redirect('/tvshow/%d/s%de%d/' % (show_id, season_no, episode_no))
