from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM MOVIE")
    rows=cursor.fetchall()
