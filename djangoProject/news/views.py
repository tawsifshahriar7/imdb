from django.shortcuts import render, redirect
from django.db import connection


def process(request):
    with connection.cursor() as cursor:
        sql = "SELECT GEN_NEWS('s',NEWS_ID),SHOW_ID,SEASON_NO, NULL AS EP_NO, TO_CHAR(TIME,'dd mon, YYYY'), TIME FROM NEWS_SEASON UNION SELECT GEN_NEWS('e',NEWS_E_ID), SHOW_ID, SEASON_NO, EPISODE_NO AS EP_NO, TO_CHAR(TIME,'dd mon, YYYY'), TIME FROM NEWS_EPISODE ORDER BY TIME DESC"
        cursor.execute(sql)
        all_news = cursor.fetchall()
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
        is_superuser = request.COOKIES['isSuperUser']
    except KeyError:
        username = None
        loggedin = False
        is_superuser = False
    user = [username, loggedin, is_superuser]
    return render(request, 'news_list.html', {"all_news": all_news, "user": user})
