from django.shortcuts import render, redirect
from django.db import connection
from django.http import Http404, HttpResponseRedirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage


def process(request):
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
        is_superuser = request.COOKIES['isSuperUser']
    except KeyError:
        username = None
        loggedin = False
        is_superuser = False
        return redirect('/login/')
    user = [username, loggedin, is_superuser]
    with connection.cursor() as cursor:
        sql = "select PHOTO from USER_IMDB where HANDLE='%s'" % username
        cursor.execute(sql)
        propic_url = cursor.fetchall()
        sql = "select RATING,M2.NAME,M2.MOVIE_ID from MOVIE_REVIEWS M join MOVIE M2 on M2.MOVIE_ID = M.MOVIE_ID where HANDLE='%s' AND RATING IS NOT NULL" % username
        cursor.execute(sql)
        rating = cursor.fetchall()
        sql = "SELECT RATING,TS.NAME,TS.SHOW_ID from TV_REVIEWS join TV_SHOW TS on TS.SHOW_ID = TV_REVIEWS.SHOW_ID where HANDLE='%s' AND RATING IS NOT NULL" % username
        cursor.execute(sql)
        rating2 = cursor.fetchall()
        sql = "select REVIEW_TEXT,M2.NAME,M2.MOVIE_ID from MOVIE_REVIEWS M join MOVIE M2 on M2.MOVIE_ID = M.MOVIE_ID where HANDLE='%s'" % username
        cursor.execute(sql)
        review = cursor.fetchall()
        sql = "SELECT REVIEW_TEXT,TS.NAME,TS.SHOW_ID from TV_REVIEWS join TV_SHOW TS on TS.SHOW_ID = TV_REVIEWS.SHOW_ID where HANDLE='%s'" % username
        cursor.execute(sql)
        review2 = cursor.fetchall()
        sql = "SELECT T.SHOW_ID, T.NAME FROM EPISODE_REVIEWS ER JOIN TV_SHOW T ON ER.SHOW_ID = T.SHOW_ID JOIN TV_REVIEWS TR ON TR.SHOW_ID = ER.SHOW_ID AND TR.HANDLE = ER.HANDLE WHERE ER.REVIEW_TEXT IS NOT NULL AND TR.REVIEW_TEXT IS NULL AND ER.HANDLE='%s' GROUP BY T.SHOW_ID, T.NAME" % username
        cursor.execute(sql)
        ep_reviewed = cursor.fetchall()
        sql = "SELECT T.SHOW_ID, T.NAME FROM EPISODE_REVIEWS ER JOIN TV_SHOW T ON ER.SHOW_ID = T.SHOW_ID JOIN TV_REVIEWS TR ON TR.SHOW_ID = ER.SHOW_ID AND TR.HANDLE = ER.HANDLE WHERE ER.RATING IS NOT NULL AND TR.RATING IS NULL AND ER.HANDLE='%s' GROUP BY T.SHOW_ID, T.NAME" % username
        cursor.execute(sql)
        ep_rated = cursor.fetchall()
        sql = "select MW.HANDLE,MW.MOVIE_ID,M.NAME from MOVIE_WATCHLIST MW join MOVIE M on M.MOVIE_ID = MW.MOVIE_ID where MW.HANDLE='%s' and MW.STATUS='True'" % username
        cursor.execute(sql)
        movie_watchlist = cursor.fetchall()
        sql = "select TW.HANDLE,TW.SHOW_ID,T.NAME from TV_SHOW_WATCHLIST TW join TV_SHOW T on T.SHOW_ID = TW.SHOW_ID where TW.HANDLE='%s' and TW.STATUS='True'" % username
        cursor.execute(sql)
        show_watchlist = cursor.fetchall()
        watchlist = [movie_watchlist, show_watchlist]
    return render(request, 'profile.html', {"user": user, "propic": propic_url, "movie_rating": rating, "show_rating": rating2, "movie_review": review, "show_review": review2, "watchlist": watchlist, "ep_rated": ep_rated, "ep_reviewed": ep_reviewed})


def edit_profile(request):
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
        is_superuser = request.COOKIES['isSuperUser']
    except KeyError:
        username = None
        loggedin = False
        is_superuser = False
    user = [username, loggedin, is_superuser]
    return render(request, 'edit_profile.html', {"user": user})


def upload(request):
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
        is_superuser = request.COOKIES['isSuperUser']
    except KeyError:
        username = None
        loggedin = False
        is_superuser = False
    user = [username, loggedin, is_superuser]
    response = redirect('/profile/')
    if request.method == 'POST':
        old_pass = request.POST['old_pass']
        new_handle = request.POST['new_username']
        new_pass = request.POST['new_pass']
        with connection.cursor() as cursor:
            sql = "SELECT PASSWORD FROM USER_IMDB WHERE HANDLE='%s'" % username
            cursor.execute(sql)
            user_pass = cursor.fetchall()
            if not old_pass:
                msg = 'Field is Empty'
                return render(request, 'edit_profile.html', {"user": user, "msg": msg})
            if old_pass != user_pass[0][0]:
                msg = 'Enter Correct Password'
                return render(request, 'edit_profile.html', {"user": user, "msg": msg})
        if request.FILES.get('propic', False):
            propic = request.FILES['propic']
            fs = FileSystemStorage()
            pic_name = fs.save(propic.name, propic)
            pic_url = fs.url(pic_name)
            with connection.cursor() as cursor:
                sql = "UPDATE USER_IMDB SET PHOTO='%s' WHERE HANDLE='%s'" % (pic_url, username)
                cursor.execute(sql)
                connection.commit()
        if new_pass:
            with connection.cursor() as cursor:
                sql = "UPDATE USER_IMDB SET PASSWORD='%s' WHERE HANDLE='%s'" % (new_pass, username)
                cursor.execute(sql)
                connection.commit()
        if new_handle:
            with connection.cursor() as cursor:
                sql = 'SELECT HANDLE FROM USER_IMDB'
                cursor.execute(sql)
                all_handle = cursor.fetchall()
                for handle in all_handle:
                    if new_handle == handle[0]:
                        msg2 = 'Username Already Exists'
                        return render(request, 'edit_profile.html', {"user": user, "msg2": msg2})
                sql = "SELECT * FROM USER_IMDB WHERE HANDLE='%s'" % username
                cursor.execute(sql)
                prev_data = cursor.fetchall()
                sql = "SELECT * FROM MOVIE_REVIEWS WHERE HANDLE='%s'" % username
                cursor.execute(sql)
                prev_movie_reviews = cursor.fetchall()
                sql = "SELECT * FROM TV_REVIEWS WHERE HANDLE='%s'" % username
                cursor.execute(sql)
                prev_show_reviews = cursor.fetchall()
                sql = "SELECT * FROM EPISODE_REVIEWS WHERE HANDLE='%s'" % username
                cursor.execute(sql)
                prev_ep_reviews = cursor.fetchall()
                sql = "SELECT * FROM MOVIE_WATCHLIST WHERE HANDLE='%s'" % username
                cursor.execute(sql)
                prev_movie_watchlist = cursor.fetchall()
                sql = "SELECT * FROM TV_SHOW_WATCHLIST WHERE HANDLE='%s'" % username
                cursor.execute(sql)
                prev_show_watchlist = cursor.fetchall()
                sql = "DELETE FROM MOVIE_REVIEWS WHERE HANDLE='%s'" % username
                cursor.execute(sql)
                connection.commit()
                sql = "DELETE FROM TV_REVIEWS WHERE HANDLE='%s'" % username
                cursor.execute(sql)
                connection.commit()
                sql = "DELETE FROM EPISODE_REVIEWS WHERE HANDLE='%s'" % username
                cursor.execute(sql)
                connection.commit()
                sql = "DELETE FROM MOVIE_WATCHLIST WHERE HANDLE='%s'" % username
                cursor.execute(sql)
                connection.commit()
                sql = "DELETE FROM TV_SHOW_WATCHLIST WHERE HANDLE='%s'" % username
                cursor.execute(sql)
                connection.commit()
                sql = "DELETE FROM USER_IMDB WHERE HANDLE='%s'" % username
                cursor.execute(sql)
                connection.commit()
                sql = "INSERT INTO USER_IMDB(HANDLE, EMAIL, PASSWORD, PHOTO, SUPERUSER) VALUES ('%s', '%s', '%s', '%s', '%s')" % (new_handle, prev_data[0][1], prev_data[0][2], prev_data[0][3], prev_data[0][5])
                cursor.execute(sql)
                connection.commit()
                for r in prev_movie_reviews:
                    sql = "INSERT INTO MOVIE_REVIEWS(MOVIE_ID, HANDLE) VALUES (%d, '%s')" % (r[0], new_handle)
                    cursor.execute(sql)
                    connection.commit()
                    if bool(r[2]):
                        sql = "UPDATE MOVIE_REVIEWS SET RATING=%d WHERE MOVIE_ID=%d AND HANDLE='%s'" % (r[2], r[0], new_handle)
                        cursor.execute(sql)
                        connection.commit()
                    if bool(r[3]):
                        sql = "UPDATE MOVIE_REVIEWS SET REVIEW_TEXT='%s' WHERE MOVIE_ID=%d AND HANDLE='%s'" % (r[3], r[0], new_handle)
                        cursor.execute(sql)
                        connection.commit()
                for r in prev_show_reviews:
                    sql = "INSERT INTO TV_REVIEWS(SHOW_ID, HANDLE) VALUES (%d, '%s')" % (r[0], new_handle)
                    cursor.execute(sql)
                    connection.commit()
                    if bool(r[2]):
                        sql = "UPDATE TV_REVIEWS SET RATING=%d WHERE SHOW_ID=%d AND HANDLE='%s'" % (r[2], r[0], new_handle)
                        cursor.execute(sql)
                        connection.commit()
                    if bool(r[3]):
                        sql = "UPDATE TV_REVIEWS SET REVIEW_TEXT='%s' WHERE SHOW_ID=%d AND HANDLE='%s'" % (r[3], r[0], new_handle)
                        cursor.execute(sql)
                        connection.commit()
                for r in prev_ep_reviews:
                    sql = "INSERT INTO EPISODE_REVIEWS(SHOW_ID, SEASON_NO, EPISODE_NO, HANDLE) VALUES (%d, %d, %d, '%s')" % (r[0], r[1], r[2], new_handle)
                    cursor.execute(sql)
                    connection.commit()
                    if bool(r[4]):
                        sql = "UPDATE EPISODE_REVIEWS SET RATING=%d WHERE SHOW_ID=%d AND SEASON_NO=%d AND EPISODE_NO=%d AND HANDLE='%s'" % (r[4], r[0], r[1], r[2], new_handle)
                        cursor.execute(sql)
                        connection.commit()
                    if bool(r[5]):
                        sql = "UPDATE EPISODE_REVIEWS SET REVIEW_TEXT='%s' WHERE SHOW_ID=%d AND SEASON_NO=%d AND EPISODE_NO=%d AND HANDLE='%s'" % (r[5], r[0], r[1], r[2], new_handle)
                        cursor.execute(sql)
                        connection.commit()
                for w in prev_movie_watchlist:
                    sql = "INSERT INTO MOVIE_WATCHLIST VALUES (%d, '%s', '%s')" % (w[0], new_handle, w[2])
                    cursor.execute(sql)
                    connection.commit()
                for w in prev_show_watchlist:
                    sql = "INSERT INTO TV_SHOW_WATCHLIST VALUES (%d, '%s', '%s')" % (w[0], new_handle, w[2])
                    cursor.execute(sql)
                    connection.commit()
            response.set_cookie('username', new_handle)
    return response


def logout(request):
    response = redirect('/')
    response.delete_cookie('username')
    response.delete_cookie('isLoggedIn')
    response.delete_cookie('isSuperUser')
    return response


def public(request, handle):
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
        sql = "select handle,photo from user_imdb where handle = '%s'" % handle
        cursor.execute(sql)
        profile = cursor.fetchall()
        if len(profile) == 0:
            raise Http404
        sql = "select REVIEW_TEXT,M2.NAME,M2.MOVIE_ID from MOVIE_REVIEWS M join MOVIE M2 on M2.MOVIE_ID = M.MOVIE_ID where HANDLE='%s'" % handle
        cursor.execute(sql)
        review = cursor.fetchall()
        sql = "SELECT REVIEW_TEXT,TS.NAME,TS.SHOW_ID from TV_REVIEWS join TV_SHOW TS on TS.SHOW_ID = TV_REVIEWS.SHOW_ID where HANDLE='%s'" % handle
        cursor.execute(sql)
        review2 = cursor.fetchall()
    return render(request, 'public_profile.html', {"user": user, "profile": profile, "movie_review": review, "show_review": review2})


def episode_section(request,show_id):
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
        is_superuser = request.COOKIES['isSuperUser']
    except KeyError:
        username = None
        loggedin = False
        is_superuser = False
        return redirect('/login/')
    user = [username, loggedin, is_superuser]
    with connection.cursor() as cursor:
        sql = "SELECT E.SHOW_ID, E.SEASON_NO, E.EPISODE_NO, E.EPISODE_NAME, ER.RATING FROM EPISODE_REVIEWS ER JOIN EPISODE E ON E.SHOW_ID = ER.SHOW_ID AND E.SEASON_NO = ER.SEASON_NO AND E.EPISODE_NO = ER.EPISODE_NO WHERE E.SHOW_ID=%d AND ER.HANDLE='%s' AND ER.RATING IS NOT NULL" % (show_id, username)
        cursor.execute(sql)
        ep_rating = cursor.fetchall()
        sql = "SELECT E.SHOW_ID, E.SEASON_NO, E.EPISODE_NO, E.EPISODE_NAME, ER.REVIEW_TEXT FROM EPISODE_REVIEWS ER JOIN EPISODE E ON E.SHOW_ID = ER.SHOW_ID AND E.SEASON_NO = ER.SEASON_NO AND E.EPISODE_NO = ER.EPISODE_NO WHERE E.SHOW_ID=%d AND ER.HANDLE='%s'" % (show_id, username)
        cursor.execute(sql)
        ep_review = cursor.fetchall()
    return render(request, 'profile_episode.html', {"user": user, "ep_rating": ep_rating, "ep_review": ep_review})
