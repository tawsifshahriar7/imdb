from django.shortcuts import render, redirect
from django.db import connection


def process(request):
    with connection.cursor() as cursor:
        sql = 'SELECT SHOW_ID, NAME, TO_CHAR(RELEASE_DATE,\'YYYY\'), POSTER, TRATING(SHOW_ID) FROM TV_SHOW'
        cursor.execute(sql)
        tv_shows = cursor.fetchall()
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
        is_superuser = request.COOKIES['isSuperUser']
    except KeyError:
        username = None
        loggedin = False
        is_superuser = False
    user = [username, loggedin, is_superuser]
    return render(request, 'tv_show.html', {"tv_shows": tv_shows, "user": user})


def sort_list(request):
    option = int(request.POST['sort_type'])
    with connection.cursor() as cursor:
        if option == 1:
            sql = 'SELECT SHOW_ID, NAME, TO_CHAR(RELEASE_DATE,\'YYYY\'), POSTER, TRATING(SHOW_ID) AS TRATE FROM TV_SHOW ORDER BY TRATE DESC'
        elif option == 2:
            sql = 'SELECT SHOW_ID, NAME, TO_CHAR(RELEASE_DATE,\'YYYY\'), POSTER, TRATING(SHOW_ID) FROM TV_SHOW ORDER BY RELEASE_DATE'
        cursor.execute(sql)
        tv_shows = cursor.fetchall()
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
        is_superuser = request.COOKIES['isSuperUser']
    except KeyError:
        username = None
        loggedin = False
        is_superuser = False
    user = [username, loggedin, is_superuser]
    return render(request, 'tv_show.html', {"tv_shows": tv_shows, "user": user})


def season_list(request, show_id, season_no):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM EPISODE WHERE SHOW_ID = %d AND SEASON_NO = %d AND EPISODE_NAME IS NOT NULL" % (show_id, season_no)
        cursor.execute(sql)
        episodes = cursor.fetchall()
        sql = "SELECT SEASON_NO FROM EPISODE WHERE SHOW_ID = %d GROUP BY SEASON_NO" % show_id
        cursor.execute(sql)
        seasons = cursor.fetchall()
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
        is_superuser = request.COOKIES['isSuperUser']
    except KeyError:
        username = None
        loggedin = False
        is_superuser = False
    user = [username, loggedin, is_superuser]
    return render(request, 'episode_list.html', {"episodes": episodes, "seasons": seasons, "show_id": show_id, "season_no": season_no, "user": user})


def select_season_list(request, show_id):
    season_no = int(request.POST['season_select'])
    with connection.cursor() as cursor:
        sql = "SELECT * FROM EPISODE WHERE SHOW_ID = %d AND SEASON_NO = %d AND EPISODE_NAME IS NOT NULL" % (show_id, season_no)
        cursor.execute(sql)
        episodes = cursor.fetchall()
        sql = "SELECT SEASON_NO FROM EPISODE WHERE SHOW_ID = %d GROUP BY SEASON_NO" % show_id
        cursor.execute(sql)
        seasons = cursor.fetchall()
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
        is_superuser = request.COOKIES['isSuperUser']
    except KeyError:
        username = None
        loggedin = False
        is_superuser = False
    user = [username, loggedin, is_superuser]
    return render(request, 'episode_list.html', {"episodes": episodes, "seasons": seasons, "show_id": show_id, "season_no": season_no, "user": user})


def detail(request, show_id):
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
        is_superuser = request.COOKIES['isSuperUser']
    except KeyError:
        username = None
        loggedin = False
        is_superuser = False
    user = [username, loggedin, is_superuser]
    with connection.cursor() as cursor:
        sql = "SELECT SHOW_ID, NAME, GENRE, SYNOPSIS, TO_CHAR(RELEASE_DATE,\'dd mon, yyyy\'), LANGUAGE, POSTER,TRATING(SHOW_ID) FROM TV_SHOW WHERE SHOW_ID=%d" % show_id
        cursor.execute(sql)
        tv_show = cursor.fetchall()
        sql = "SELECT TR.HANDLE, TR.RATING,TR.REVIEW_TEXT from TV_SHOW T join TV_REVIEWS TR on T.SHOW_ID = TR.SHOW_ID where T.SHOW_ID=%d" % show_id
        cursor.execute(sql)
        reviews = cursor.fetchall()
        sql = "select C.CELEB_ID,C.NAME from TV_SHOW T join TV_DIRECTOR TD on T.SHOW_ID = TD.SHOW_ID join CELEB C on C.CELEB_ID = TD.CELEB_ID where T.SHOW_ID = %d" % show_id
        cursor.execute(sql)
        director = cursor.fetchall()
        sql = "select C.CELEB_ID,C.NAME from TV_SHOW T join TV_ACTOR TD on T.SHOW_ID = TD.SHOW_ID join CELEB C on C.CELEB_ID = TD.CELEB_ID where T.SHOW_ID = %d" % show_id
        cursor.execute(sql)
        actors = cursor.fetchall()
        sql = "select C.CELEB_ID,C.NAME from TV_SHOW T join TV_WRITER TD on T.SHOW_ID = TD.SHOW_ID join CELEB C on C.CELEB_ID = TD.CELEB_ID where T.SHOW_ID = %d" % show_id
        cursor.execute(sql)
        writer = cursor.fetchall()
        sql = "select C.CELEB_ID,C.NAME from TV_SHOW T join TV_PRODUCER TD on T.SHOW_ID = TD.SHOW_ID join CELEB C on C.CELEB_ID = TD.CELEB_ID where T.SHOW_ID = %d" % show_id
        cursor.execute(sql)
        producer = cursor.fetchall()
        sql = "SELECT STATUS FROM TV_SHOW_WATCHLIST WHERE SHOW_ID=%d AND HANDLE='%s'" % (show_id, username)
        cursor.execute(sql)
        status = cursor.fetchall()
        sql = "SELECT SEASON_NO FROM EPISODE WHERE SHOW_ID = %d GROUP BY SEASON_NO" % show_id
        cursor.execute(sql)
        seasons = cursor.fetchall()
        sql = "SELECT COUNT(*) FROM EPISODE WHERE SHOW_ID = %d AND EPISODE_NAME IS NOT NULL" % show_id
        cursor.execute(sql)
        episode_no = cursor.fetchall()
        if len(status) == 0:
            status = False
        elif status[0][0] == 'True':
            status = True
        else:
            status = False
    return render(request, 'show_detail.html', {"tv_show": tv_show, "user": user, "reviews": reviews, "director": director, "actors": actors, "writer": writer, "producer": producer, "status": status, "seasons": seasons, "episodeNo": episode_no})


def episode_detail(request, show_id, season_no, episode_no):
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
        is_superuser = request.COOKIES['isSuperUser']
    except KeyError:
        username = None
        loggedin = False
        is_superuser = False
    user = [username, loggedin, is_superuser]
    with connection.cursor() as cursor:
        sql = "SELECT SHOW_ID, SEASON_NO, EPISODE_NO, EPISODE_NAME, SYNOPSIS, TO_CHAR(RELEASE_DATE, \'dd mon, yyyy\'), convert_runtime(RUNTIME), POSTER,ERATING(SHOW_ID,SEASON_NO,EPISODE_NO) FROM EPISODE WHERE SHOW_ID=%d AND SEASON_NO = %d AND EPISODE_NO = %d" % (show_id, season_no, episode_no)
        cursor.execute(sql)
        ep_info = cursor.fetchall()
        sql = "SELECT NAME FROM TV_SHOW WHERE SHOW_ID = %d" % show_id
        cursor.execute(sql)
        show_name = cursor.fetchall()
        sql = "select C.CELEB_ID,C.NAME from EPISODE E join EPISODE_DIRECTOR ED on E.SHOW_ID = ED.SHOW_ID and E.SEASON_NO = ED.SEASON_NO and E.EPISODE_NO = ED.EPISODE_NO join CELEB C on C.CELEB_ID = ED.CELEB_ID where E.SHOW_ID = %d and E.SEASON_NO = %d and E.EPISODE_NO = %d" % (show_id, season_no, episode_no)
        cursor.execute(sql)
        director = cursor.fetchall()
        sql = "select C.CELEB_ID,C.NAME from EPISODE E join EPISODE_ACTOR ED on E.SHOW_ID = ED.SHOW_ID and E.SEASON_NO = ED.SEASON_NO and E.EPISODE_NO = ED.EPISODE_NO join CELEB C on C.CELEB_ID = ED.CELEB_ID where E.SHOW_ID = %d and E.SEASON_NO = %d and E.EPISODE_NO = %d" % (
        show_id, season_no, episode_no)
        cursor.execute(sql)
        actors = cursor.fetchall()
        sql = "select C.CELEB_ID,C.NAME from EPISODE E join EPISODE_WRITER ED on E.SHOW_ID = ED.SHOW_ID and E.SEASON_NO = ED.SEASON_NO and E.EPISODE_NO = ED.EPISODE_NO join CELEB C on C.CELEB_ID = ED.CELEB_ID where E.SHOW_ID = %d and E.SEASON_NO = %d and E.EPISODE_NO = %d" % (
        show_id, season_no, episode_no)
        cursor.execute(sql)
        writer = cursor.fetchall()
        sql = "SELECT ER.HANDLE, ER.RATING,ER.REVIEW_TEXT from EPISODE E join EPISODE_REVIEWS ER on E.SHOW_ID = ER.SHOW_ID and E.SEASON_NO = ER.SEASON_NO AND E.EPISODE_NO = ER.EPISODE_NO where E.SHOW_ID=%d and E.SEASON_NO=%d and E.EPISODE_NO=%d" % (show_id, season_no, episode_no)
        cursor.execute(sql)
        reviews = cursor.fetchall()
    return render(request, 'episode_detail.html', {"ep": ep_info, "show_name": show_name, "director": director, "actors": actors, "writer": writer, "reviews": reviews, "user": user})


def submit_rating(request, show_id):
    rating = int(request.POST['rating'])
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
            sql = "INSERT INTO TV_REVIEWS (SHOW_ID, HANDLE, RATING) VALUES(%d,'%s', %d)" % (show_id, username, rating)
        else:
            sql = "UPDATE TV_REVIEWS SET RATING=%d WHERE SHOW_ID=%d AND HANDLE='%s'" % (rating, show_id, username)
        cursor.execute(sql)
        connection.commit()
    return redirect('/tvshow/%d/' % show_id)


def episode_rating(request, show_id, season_no, episode_no):
    rating = int(request.POST['rating'])
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
    except KeyError:
        return redirect('/login/')
    with connection.cursor() as cursor:
        sql = "SELECT * FROM EPISODE_REVIEWS WHERE HANDLE = '%s' AND SHOW_ID = %d AND SEASON_NO = %d AND EPISODE_NO = %d" % (username, show_id, season_no, episode_no)
        cursor.execute(sql)
        previous_review = cursor.fetchall()
        if len(previous_review) == 0:
            sql = "INSERT INTO EPISODE_REVIEWS (SHOW_ID, SEASON_NO, EPISODE_NO, HANDLE, RATING) VALUES(%d, %d, %d, '%s', %d)" % (show_id, season_no, episode_no, username, rating)
        else:
            sql = "UPDATE EPISODE_REVIEWS SET RATING=%d WHERE SHOW_ID=%d AND SEASON_NO = %d AND EPISODE_NO = %d AND HANDLE='%s'" % (rating, show_id, season_no, episode_no, username)
        cursor.execute(sql)
        connection.commit()
        sql = "SELECT * FROM TV_REVIEWS WHERE HANDLE='%s' AND SHOW_ID=%d" % (username, show_id)
        cursor.execute(sql)
        previous_review = cursor.fetchall()
        if len(previous_review) == 0:
            sql = "INSERT INTO TV_REVIEWS (SHOW_ID, HANDLE) VALUES(%d,'%s')" % (show_id, username)
            cursor.execute(sql)
            connection.commit()
    return redirect('/tvshow/%d/%d/%d/' % (show_id, season_no, episode_no))


def submit_review(request, show_id):
    review_text = request.POST['review_text']
    review_text = review_text.replace("'", "''")
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
            sql = "INSERT INTO TV_REVIEWS(SHOW_ID,HANDLE,REVIEW_TEXT) VALUES(%d,'%s','%s')" % (show_id, username, review_text)
        else:
            sql = "UPDATE TV_REVIEWS SET REVIEW_TEXT='%s' WHERE SHOW_ID=%d AND HANDLE='%s'" % (review_text, show_id, username)
        cursor.execute(sql)
        connection.commit()
    return redirect('/tvshow/%d/' % show_id)


def episode_review(request, show_id, season_no, episode_no):
    review_text = request.POST['review_text']
    review_text = review_text.replace("'", "''")
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
    except KeyError:
        return redirect('/login/')
    with connection.cursor() as cursor:
        sql = "SELECT * FROM EPISODE_REVIEWS WHERE HANDLE = '%s' AND SHOW_ID = %d AND SEASON_NO = %d AND EPISODE_NO = %d" % (username, show_id, season_no, episode_no)
        cursor.execute(sql)
        previous_review = cursor.fetchall()
        if len(previous_review) == 0:
            sql = "INSERT INTO EPISODE_REVIEWS (SHOW_ID, SEASON_NO, EPISODE_NO, HANDLE, REVIEW_TEXT) VALUES(%d, %d, %d, '%s', '%s')" % (show_id, season_no, episode_no, username, review_text)
        else:
            sql = "UPDATE EPISODE_REVIEWS SET REVIEW_TEXT='%s' WHERE SHOW_ID=%d AND SEASON_NO = %d AND EPISODE_NO = %d AND HANDLE='%s'" % (review_text, show_id, season_no, episode_no, username)
        cursor.execute(sql)
        connection.commit()
        sql = "SELECT * FROM TV_REVIEWS WHERE HANDLE='%s' AND SHOW_ID=%d" % (username, show_id)
        cursor.execute(sql)
        previous_review = cursor.fetchall()
        if len(previous_review) == 0:
            sql = "INSERT INTO TV_REVIEWS (SHOW_ID, HANDLE) VALUES(%d,'%s')" % (show_id, username)
            cursor.execute(sql)
            connection.commit()
    return redirect('/tvshow/%d/%d/%d/' % (show_id, season_no, episode_no))


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

