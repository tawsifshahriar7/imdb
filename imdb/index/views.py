from django.shortcuts import render


def process(request):
    username = request.COOKIES['username']
    loggedin = request.COOKIES['isLoggedIn']
    user = [username, loggedin]
    context = {"user": user}
    print(context)
    return render(request, 'index.html', {"user": user})

