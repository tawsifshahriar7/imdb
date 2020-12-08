from django.shortcuts import render, redirect
from django.db import connection
from django.http import Http404
from django.contrib import messages


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
        if username is not None:
            sql = "SELECT * FROM USER_IMDB WHERE HANDLE='%s'" % username
            cursor.execute(sql)
            profile_data = cursor.fetchall()
        sql = "select M.MOVIE_ID,M.NAME,MR.RATING,MR.REVIEW_TEXT from MOVIE_REVIEWS MR join MOVIE M on M.MOVIE_ID = MR.MOVIE_ID where MR.HANDLE='%s'" % username
        cursor.execute(sql)
        m_review = cursor.fetchall()
        sql = "select T.SHOW_ID,T.NAME,TR.RATING,TR.REVIEW_TEXT from TV_REVIEWS TR join TV_SHOW T on T.SHOW_ID = TR.SHOW_ID where TR.HANDLE='%s'" % username
        cursor.execute(sql)
        t_review = cursor.fetchall()
        sql = "select MW.HANDLE,MW.MOVIE_ID,M.NAME from MOVIE_WATCHLIST MW join MOVIE M on M.MOVIE_ID = MW.MOVIE_ID where MW.HANDLE='%s' and MW.STATUS='True'" % username
        cursor.execute(sql)
        movie_watchlist = cursor.fetchall()
        sql = "select TW.HANDLE,TW.SHOW_ID,T.NAME from TV_SHOW_WATCHLIST TW join TV_SHOW T on T.SHOW_ID = TW.SHOW_ID where TW.HANDLE='%s' and TW.STATUS='True'" % username
        cursor.execute(sql)
        show_watchlist = cursor.fetchall()
        watchlist = [movie_watchlist, show_watchlist]
    return render(request, 'profile.html', {"user": user, "profile_data": profile_data, "m_review": m_review, "t_review": t_review, "watchlist": watchlist})


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


def change_dp(request, handle):
    return render(request, 'dp_change_form.html', {"user": handle})


def dp_changed(request, handle):
    picture = request.POST['new_pic']
    password = request.POST['password']
    with connection.cursor() as cursor:
        sql = "SELECT PASSWORD FROM USER_IMDB WHERE HANDLE='%s'" % handle
        cursor.execute(sql)
        user_pass = cursor.fetchall()
        if user_pass[0][0] == password:
            sql = "UPDATE USER_IMDB SET PHOTO='%s' WHERE HANDLE='%s'" % (picture, handle)
            cursor.execute(sql)
            connection.commit()
            return redirect('/profile/')
        else:
            messages.error(request, 'Password Incorrect')
            return redirect('/profile/id=%s/change_picture/' % handle)


def change_pass(request, handle):
    return render(request, 'pass_change_form.html', {"user": handle})


def pass_changed(request, handle):
    old_pass = request.POST['old_pass']
    new_pass = request.POST['new_pass']
    new_pass2 = request.POST['new_pass2']
    with connection.cursor() as cursor:
        sql = "SELECT PASSWORD FROM USER_IMDB WHERE HANDLE='%s'" % handle
        cursor.execute(sql)
        comp = cursor.fetchall()
        if comp[0][0] == old_pass:
            if new_pass == new_pass2:
                sql = "UPDATE USER_IMDB SET PASSWORD='%s' WHERE HANDLE='%s'" % (new_pass, handle)
                cursor.execute(sql)
                connection.commit()
                return redirect('/login/')
            else:
                messages.error(request, 'Passwords did not match')
                return redirect('/profile/id=%s/change_password/' % handle)
        else:
            messages.error(request, 'Incorrect Password')
            return redirect('/profile/id=%s/change_password/' % handle)
