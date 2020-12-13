from django.shortcuts import render
from django.db import connection


def process(request):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM CELEB"
        cursor.execute(sql)
        celebs = cursor.fetchall()
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
        is_superuser = request.COOKIES['isSuperUser']
    except KeyError:
        username = None
        loggedin = False
        is_superuser = False
    user = [username, loggedin, is_superuser]
    return render(request, 'celeb.html', {"celebs": celebs, "user": user})


def detail(request, celeb_id):
    with connection.cursor() as cursor:
        sql = "SELECT CELEB_ID, NAME, PHOTO, TO_CHAR(BIRTHDAY, \'dd mon, yyyy\'), TO_CHAR(DEATHDAY, \'dd mon, yyyy\'), BIOGRAPHY, HEIGHT FROM CELEB WHERE CELEB_ID=%d" % celeb_id
        cursor.execute(sql)
        celeb = cursor.fetchall()
        sql = "SELECT M.MOVIE_ID, M.NAME FROM CELEB C JOIN MOVIE_ACTOR MA ON C.CELEB_ID = MA.CELEB_ID JOIN MOVIE M ON MA.MOVIE_ID = M.MOVIE_ID WHERE C.CELEB_ID = %d" % celeb_id
        cursor.execute(sql)
        acted_movie = cursor.fetchall()
        sql = "SELECT T.SHOW_ID, T.NAME FROM CELEB C JOIN TV_ACTOR TA ON C.CELEB_ID = TA.CELEB_ID JOIN TV_SHOW T ON TA.SHOW_ID = T.SHOW_ID WHERE C.CELEB_ID = %d" % celeb_id
        cursor.execute(sql)
        acted_show = cursor.fetchall()
        sql = "SELECT M.MOVIE_ID, M.NAME FROM CELEB C JOIN MOVIE_DIRECTOR MA ON C.CELEB_ID = MA.CELEB_ID JOIN MOVIE M ON MA.MOVIE_ID = M.MOVIE_ID WHERE C.CELEB_ID = %d" % celeb_id
        cursor.execute(sql)
        directed_movie = cursor.fetchall()
        sql = "SELECT T.SHOW_ID, T.NAME FROM CELEB C JOIN TV_DIRECTOR TA ON C.CELEB_ID = TA.CELEB_ID JOIN TV_SHOW T ON TA.SHOW_ID = T.SHOW_ID WHERE C.CELEB_ID = %d" % celeb_id
        cursor.execute(sql)
        directed_show = cursor.fetchall()
        sql = "SELECT M.MOVIE_ID, M.NAME FROM CELEB C JOIN MOVIE_WRITER MA ON C.CELEB_ID = MA.CELEB_ID JOIN MOVIE M ON MA.MOVIE_ID = M.MOVIE_ID WHERE C.CELEB_ID = %d" % celeb_id
        cursor.execute(sql)
        wrote_movie = cursor.fetchall()
        sql = "SELECT T.SHOW_ID, T.NAME FROM CELEB C JOIN TV_WRITER TA ON C.CELEB_ID = TA.CELEB_ID JOIN TV_SHOW T ON TA.SHOW_ID = T.SHOW_ID WHERE C.CELEB_ID = %d" % celeb_id
        cursor.execute(sql)
        wrote_show = cursor.fetchall()
        sql = "SELECT M.MOVIE_ID, M.NAME FROM CELEB C JOIN MOVIE_PRODUCER MA ON C.CELEB_ID = MA.CELEB_ID JOIN MOVIE M ON MA.MOVIE_ID = M.MOVIE_ID WHERE C.CELEB_ID = %d" % celeb_id
        cursor.execute(sql)
        produced_movie = cursor.fetchall()
        sql = "SELECT T.SHOW_ID, T.NAME FROM CELEB C JOIN TV_PRODUCER TA ON C.CELEB_ID = TA.CELEB_ID JOIN TV_SHOW T ON TA.SHOW_ID = T.SHOW_ID WHERE C.CELEB_ID = %d" % celeb_id
        cursor.execute(sql)
        produced_show = cursor.fetchall()
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
        is_superuser = request.COOKIES['isSuperUser']
    except KeyError:
        username = None
        loggedin = False
        is_superuser = False
    user = [username, loggedin, is_superuser]
    return render(request, 'detail.html', {"celeb": celeb, "acted_movie": acted_movie, "acted_show": acted_show, "directed_movie": directed_movie, "directed_show": directed_show, "wrote_movie": wrote_movie, "wrote_show": wrote_show, "produced_movie": produced_movie, "produced_show": produced_show, "user": user})


def celeb_ep_list(request, celeb_id, show_id, role):
    with connection.cursor() as cursor:
        sql = "SELECT CELEB_ID, NAME FROM CELEB WHERE CELEB_ID=%d " % celeb_id
        cursor.execute(sql)
        celeb_name = cursor.fetchall()
        sql = "SELECT SHOW_ID, NAME FROM TV_SHOW WHERE SHOW_ID=%d " % show_id
        cursor.execute(sql)
        show_name = cursor.fetchall()
        if role == 'actor':
            sql = "SELECT E.SHOW_ID, E.SEASON_NO, E.EPISODE_NO, E.EPISODE_NAME FROM CELEB C JOIN EPISODE_ACTOR EA ON C.CELEB_ID = EA.CELEB_ID JOIN EPISODE E ON EA.SHOW_ID = E.SHOW_ID  AND EA.SEASON_NO = E.SEASON_NO AND EA.EPISODE_NO = E.EPISODE_NO WHERE C.CELEB_ID = %d AND E.SHOW_ID=%d" % (celeb_id, show_id)
            cursor.execute(sql)
            ep_career = cursor.fetchall()
        elif role == 'director':
            sql = "SELECT E.SHOW_ID, E.SEASON_NO, E.EPISODE_NO, E.EPISODE_NAME FROM CELEB C JOIN EPISODE_DIRECTOR EA ON C.CELEB_ID = EA.CELEB_ID JOIN EPISODE E ON EA.SHOW_ID = E.SHOW_ID  AND EA.SEASON_NO = E.SEASON_NO AND EA.EPISODE_NO = E.EPISODE_NO WHERE C.CELEB_ID = %d AND E.SHOW_ID=%d" % (celeb_id, show_id)
            cursor.execute(sql)
            ep_career = cursor.fetchall()
        elif role == 'writer':
            sql = "SELECT E.SHOW_ID, E.SEASON_NO, E.EPISODE_NO, E.EPISODE_NAME FROM CELEB C JOIN EPISODE_WRITER EA ON C.CELEB_ID = EA.CELEB_ID JOIN EPISODE E ON EA.SHOW_ID = E.SHOW_ID  AND EA.SEASON_NO = E.SEASON_NO AND EA.EPISODE_NO = E.EPISODE_NO WHERE C.CELEB_ID = %d AND E.SHOW_ID=%d" % (celeb_id, show_id)
            cursor.execute(sql)
            ep_career = cursor.fetchall()
        else:
            ep_career = []
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
        is_superuser = request.COOKIES['isSuperUser']
    except KeyError:
        username = None
        loggedin = False
        is_superuser = False
    user = [username, loggedin, is_superuser]
    return render(request, 'celeb_episode.html', {"user": user, "celeb_name": celeb_name, "show_name": show_name, "ep_career": ep_career})
