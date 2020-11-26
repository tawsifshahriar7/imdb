from django.shortcuts import render,redirect


def process(request):
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
    except KeyError:
        username = None
        loggedin = False
    if username == 'admin':
        return render(request, 'superuser.html')
    else:
        return redirect('/login/')
