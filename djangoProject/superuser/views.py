from django.shortcuts import render, redirect
from django.db import connection


def process(request):
    username = request.POST["Uname"]
    password = request.POST["Pass"]
    with connection.cursor() as cursor:
        sql = "SELECT HANDLE,PASSWORD,SUPERUSER FROM USER_IMDB WHERE HANDLE='%s'" % username
        cursor.execute(sql)
        cred = cursor.fetchall()
        response = redirect('/')
        if username == cred[0][0] and password == cred[0][1] and cred[0][2] == 'YES':
            loggedin = True
            is_superuser = True
            response.set_cookie('username', username)
            response.set_cookie('isLoggedIn', loggedin)
            response.set_cookie('isSuperUser', is_superuser)
        else:
            return redirect('/login/')
    return response


def profile(request):
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
        is_superuser = request.COOKIES['isSuperUser']
    except KeyError:
        username = None
        loggedin = False
        is_superuser = False
    if is_superuser == 'False':
        return redirect('/login/')
    user = [username, loggedin, is_superuser]
    return render(request, 'superuser_profile.html', {"user": user})


def movie_added(request):
    name = request.POST['movie_name']
    genre = request.POST['genre']
    synopsis = request.POST['synopsis']
    synopsis = synopsis.replace("'", "''")
    poster = request.POST['poster']
    release_date = request.POST['release_date']
    runtime = request.POST['runtime']
    runtime = int(runtime)
    language = request.POST['language']
    with connection.cursor() as cursor:
        sql = "SELECT NAME FROM MOVIE WHERE NAME='%s'" % name
        cursor.execute(sql)
        x = cursor.fetchall()
        if len(x) == 0:
            sql = "SELECT MAX(MOVIE_ID) FROM MOVIE"
            cursor.execute(sql)
            id = cursor.fetchall()
            movie_id = int(id[0][0])
            movie_id = movie_id+1
            sql = "INSERT INTO MOVIE VALUES(%d,'%s','%s','%s',TO_DATE('%s','YYYY-MM-DD'),%d,'%s','%s')" % (movie_id, name, genre, synopsis, release_date, runtime, language, poster)
            cursor.execute(sql)
            connection.commit()
    return redirect('/superuser/profile/')


def show_added(request):
    name = request.POST['show_name']
    genre = request.POST['genre']
    synopsis = request.POST['synopsis']
    synopsis = synopsis.replace("'", "''")
    poster = request.POST['poster']
    release_date = request.POST['release_date']
    language = request.POST['language']
    with connection.cursor() as cursor:
        sql = "SELECT NAME FROM TV_SHOW WHERE NAME='%s'" % name
        cursor.execute(sql)
        x = cursor.fetchall()
        if len(x) == 0:
            sql = "SELECT MAX(SHOW_ID) FROM TV_SHOW"
            cursor.execute(sql)
            id = cursor.fetchall()
            show_id = int(id[0][0])
            show_id = show_id + 1
            sql = "INSERT INTO TV_SHOW VALUES(%d,'%s','%s','%s',TO_DATE('%s','YYYY-MM-DD'),'%s','%s')" % (show_id, name, genre, synopsis, release_date, language, poster)
            cursor.execute(sql)
            connection.commit()
    return redirect('/superuser/profile/')


def celeb_added(request):
    name = request.POST['name']
    photo = request.POST['photo']
    biography = request.POST['biography']
    biography = biography.replace("'", "''")
    height = request.POST['height']
    if len(height) != 0:
        height = float(height)
    birthday = request.POST['birthday']
    deathday = request.POST['deathday']
    with connection.cursor() as cursor:
        sql = "SELECT NAME FROM CELEB WHERE NAME='%s'" % name
        cursor.execute(sql)
        x = cursor.fetchall()
        if len(x) == 0:
            sql = "SELECT MAX(CELEB_ID) FROM CELEB"
            cursor.execute(sql)
            id = cursor.fetchall()
            celeb_id = int(id[0][0])
            celeb_id = celeb_id + 1
            sql = "INSERT INTO CELEB VALUES(%d,'%s','%s',TO_DATE('%s','YYYY-MM-DD'),TO_DATE('%s','YYYY-MM-DD'),'%s','%s')" % (celeb_id, name, photo, birthday, deathday, biography, height)
            cursor.execute(sql)
            connection.commit()
    return redirect('/superuser/profile/')


def new_season(request, show_id):
    season_no = int(request.POST['addSeason'])
    season_no = season_no + 1
    ep_no = 1
    with connection.cursor() as cursor:
        sql = "SELECT SEASON_NO FROM EPISODE WHERE SHOW_ID=%d AND SEASON_NO=%d GROUP BY SEASON_NO" % (show_id, season_no)
        cursor.execute(sql)
        season_data = cursor.fetchall()
        if not bool(season_data):
            sql = "INSERT INTO EPISODE(SHOW_ID, SEASON_NO, EPISODE_NO) VALUES(%d, %d, %d)" % (show_id, season_no, ep_no)
            cursor.execute(sql)
            connection.commit()
    return redirect('/tvshow/%d/%d/' % (show_id, season_no))


def new_episode(request, show_id, season_no):
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
        is_superuser = request.COOKIES['isSuperUser']
    except KeyError:
        username = None
        loggedin = False
        is_superuser = False
    if is_superuser == 'False':
        return redirect('/login/')
    user = [username, loggedin, is_superuser]
    return render(request, 'new_episode_form.html', {"user": user, "show_id": show_id, "season_no": season_no})


def episode_added(request, show_id, season_no):
    episode_no = int(request.POST['episode_no'])
    name = request.POST['episode_name']
    synopsis = request.POST['synopsis']
    synopsis = synopsis.replace("'", "''")
    release_date = request.POST['release_date']
    runtime = int(request.POST['runtime'])
    poster = request.POST['poster']
    with connection.cursor() as cursor:
        sql = "SELECT SHOW_ID FROM EPISODE WHERE SHOW_ID=%d AND SEASON_NO=%d AND EPISODE_NO=%d" % (show_id, season_no, episode_no)
        cursor.execute(sql)
        x = cursor.fetchall()
        if len(x) == 0:
            sql = "INSERT INTO EPISODE VALUES(%d,%d,%d,'%s','%s',TO_DATE('%s','YYYY-MM-DD'),%d,'%s')" % (show_id, season_no, episode_no, name, synopsis, release_date, runtime, poster)
        else:
            sql = "UPDATE EPISODE SET EPISODE_NAME='%s', SYNOPSIS='%s', RELEASE_DATE=TO_DATE('%s','YYYY-MM-DD'), RUNTIME=%d, POSTER='%s' WHERE SHOW_ID=%d AND SEASON_NO=%d AND EPISODE_NO=%d" % (name, synopsis, release_date, runtime, poster, show_id, season_no, episode_no)
        cursor.execute(sql)
        connection.commit()
    return redirect('/tvshow/%d/%d/' % (show_id, season_no))


def celeb_update(request, celeb_id):
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
        is_superuser = request.COOKIES['isSuperUser']
    except KeyError:
        username = None
        loggedin = False
        is_superuser = False
    if is_superuser == 'False':
        return redirect('/login/')
    user = [username, loggedin, is_superuser]
    return render(request, 'celeb_career.html', {"user": user, "celeb_id": celeb_id})


def celeb_movie_update(request, celeb_id):
    name = request.POST['movie_name']
    role = request.POST['role']
    with connection.cursor() as cursor:
        sql = "SELECT MOVIE_ID FROM MOVIE WHERE NAME = '%s'" % name
        cursor.execute(sql)
        movie_dict = cursor.fetchall()
        if bool(movie_dict):
            movie_id = int(movie_dict[0][0])
            if role == 'actor':
                sql = "SELECT * FROM MOVIE_ACTOR WHERE MOVIE_ID=%d AND CELEB_ID=%d" % (movie_id, celeb_id)
                cursor.execute(sql)
                prev_data = cursor.fetchall()
                if not bool(prev_data):
                    sql = "INSERT INTO MOVIE_ACTOR VALUES(%d, %d)" % (movie_id, celeb_id)
                    cursor.execute(sql)
                    connection.commit()
            elif role == 'director':
                sql = "SELECT * FROM MOVIE_DIRECTOR WHERE MOVIE_ID=%d AND CELEB_ID=%d" % (movie_id, celeb_id)
                cursor.execute(sql)
                prev_data = cursor.fetchall()
                if not bool(prev_data):
                    sql = "INSERT INTO MOVIE_DIRECTOR VALUES(%d, %d)" % (movie_id, celeb_id)
                    cursor.execute(sql)
                    connection.commit()
            elif role == 'writer':
                sql = "SELECT * FROM MOVIE_WRITER WHERE MOVIE_ID=%d AND CELEB_ID=%d" % (movie_id, celeb_id)
                cursor.execute(sql)
                prev_data = cursor.fetchall()
                if not bool(prev_data):
                    sql = "INSERT INTO MOVIE_WRITER VALUES(%d, %d)" % (movie_id, celeb_id)
                    cursor.execute(sql)
                    connection.commit()
            elif role == 'producer':
                sql = "SELECT * FROM MOVIE_PRODUCER WHERE MOVIE_ID=%d AND CELEB_ID=%d" % (movie_id, celeb_id)
                cursor.execute(sql)
                prev_data = cursor.fetchall()
                if not bool(prev_data):
                    sql = "INSERT INTO MOVIE_PRODUCER VALUES(%d, %d)" % (movie_id, celeb_id)
                    cursor.execute(sql)
                    connection.commit()

    return redirect('/superuser/%d/celeb_edit' % celeb_id)


def celeb_show_update(request, celeb_id):
    name = request.POST['show_name']
    role = request.POST['role']
    with connection.cursor() as cursor:
        sql = "SELECT SHOW_ID FROM TV_SHOW WHERE NAME = '%s'" % name
        cursor.execute(sql)
        show_dict = cursor.fetchall()
        if bool(show_dict):
            show_id = int(show_dict[0][0])
            if role == 'actor':
                sql = "SELECT * FROM TV_ACTOR WHERE SHOW_ID=%d AND CELEB_ID=%d" % (show_id, celeb_id)
                cursor.execute(sql)
                prev_data = cursor.fetchall()
                if not bool(prev_data):
                    sql = "INSERT INTO TV_ACTOR VALUES(%d, %d)" % (show_id, celeb_id)
                    cursor.execute(sql)
                    connection.commit()
            elif role == 'director':
                sql = "SELECT * FROM TV_DIRECTOR WHERE SHOW_ID=%d AND CELEB_ID=%d" % (show_id, celeb_id)
                cursor.execute(sql)
                prev_data = cursor.fetchall()
                if not bool(prev_data):
                    sql = "INSERT INTO TV_DIRECTOR VALUES(%d, %d)" % (show_id, celeb_id)
                    cursor.execute(sql)
                    connection.commit()
            elif role == 'writer':
                sql = "SELECT * FROM TV_WRITER WHERE SHOW_ID=%d AND CELEB_ID=%d" % (show_id, celeb_id)
                cursor.execute(sql)
                prev_data = cursor.fetchall()
                if not bool(prev_data):
                    sql = "INSERT INTO TV_WRITER VALUES(%d, %d)" % (show_id, celeb_id)
                    cursor.execute(sql)
                    connection.commit()
            elif role == 'producer':
                sql = "SELECT * FROM TV_PRODUCER WHERE SHOW_ID=%d AND CELEB_ID=%d" % (show_id, celeb_id)
                cursor.execute(sql)
                prev_data = cursor.fetchall()
                if not bool(prev_data):
                    sql = "INSERT INTO TV_PRODUCER VALUES(%d, %d)" % (show_id, celeb_id)
                    cursor.execute(sql)
                    connection.commit()

    return redirect('/superuser/%d/celeb_edit' % celeb_id)


def celeb_ep_update(request, celeb_id):
    name = request.POST['show_name']
    season_no = int(request.POST['season_no'])
    episode_no = int(request.POST['episode_no'])
    role = request.POST['role']
    with connection.cursor() as cursor:
        sql = "SELECT SHOW_ID FROM TV_SHOW WHERE NAME = '%s'" % name
        cursor.execute(sql)
        show_dict = cursor.fetchall()
        show_id = int(show_dict[0][0])
        sql = "SELECT SHOW_ID, SEASON_NO, EPISODE_NO FROM EPISODE WHERE SHOW_ID=%d AND SEASON_NO=%d AND EPISODE_NO=%d" % (show_id, season_no, episode_no)
        cursor.execute(sql)
        ep_dict = cursor.fetchall()
        if bool(ep_dict):
            if role == 'actor':
                sql = "SELECT * FROM TV_ACTOR WHERE SHOW_ID=%d AND CELEB_ID=%d" % (show_id, celeb_id)
                cursor.execute(sql)
                previous_acting = cursor.fetchall()
                if not bool(previous_acting):
                    sql = "INSERT INTO TV_ACTOR VALUES(%d,%d)" % (show_id, celeb_id)
                    cursor.execute(sql)
                    connection.commit()
                sql = "SELECT * FROM EPISODE_ACTOR WHERE SHOW_ID=%d AND SEASON_NO=%d AND EPISODE_NO=%d AND CELEB_ID=%d" % (show_id, season_no, episode_no, celeb_id)
                cursor.execute(sql)
                prev_data = cursor.fetchall()
                if not bool(prev_data):
                    sql = "INSERT INTO EPISODE_ACTOR VALUES(%d, %d, %d, %d)" % (show_id, season_no, episode_no, celeb_id)
                    cursor.execute(sql)
                    connection.commit()
            elif role == 'director':
                sql = "SELECT * FROM TV_DIRECTOR WHERE SHOW_ID=%d AND CELEB_ID=%d" % (show_id, celeb_id)
                cursor.execute(sql)
                previous_directing = cursor.fetchall()
                if not bool(previous_directing):
                    sql = "INSERT INTO TV_DIRECTOR VALUES(%d,%d)" % (show_id, celeb_id)
                    cursor.execute(sql)
                    connection.commit()
                sql = "SELECT * FROM EPISODE_DIRECTOR WHERE SHOW_ID=%d AND SEASON_NO=%d AND EPISODE_NO=%d AND CELEB_ID=%d" % (show_id, season_no, episode_no, celeb_id)
                cursor.execute(sql)
                prev_data = cursor.fetchall()
                if not bool(prev_data):
                    sql = "INSERT INTO EPISODE_DIRECTOR VALUES(%d, %d, %d, %d)" % (show_id, season_no, episode_no, celeb_id)
                    cursor.execute(sql)
                    connection.commit()
            elif role == 'writer':
                sql = "SELECT * FROM TV_WRITER WHERE SHOW_ID=%d AND CELEB_ID=%d" % (show_id, celeb_id)
                cursor.execute(sql)
                previous_writing = cursor.fetchall()
                if not bool(previous_writing):
                    sql = "INSERT INTO TV_WRITER VALUES(%d,%d)" % (show_id, celeb_id)
                    cursor.execute(sql)
                    connection.commit()
                sql = "SELECT * FROM EPISODE_WRITER WHERE SHOW_ID=%d AND SEASON_NO=%d AND EPISODE_NO=%d AND CELEB_ID=%d" % (show_id, season_no, episode_no, celeb_id)
                cursor.execute(sql)
                prev_data = cursor.fetchall()
                if not bool(prev_data):
                    sql = "INSERT INTO EPISODE_WRITER VALUES(%d, %d, %d, %d)" % (show_id, season_no, episode_no, celeb_id)
                    cursor.execute(sql)
                    connection.commit()

    return redirect('/superuser/%d/celeb_edit' % celeb_id)










