from django.shortcuts import render,redirect


def process(request):
    try:
        username = request.COOKIES['username']
        loggedin = request.COOKIES['isLoggedIn']
    except KeyError:
        username = None
        loggedin = False
        return redirect('/login/')
    user = [username, loggedin]
    return render(request, 'profile.html', {"user": user})


def logout(request):
    response = render(request, 'profile.html')
    response.delete_cookie('username')
    response.delete_cookie('isLoggedIn')
    return response
