from django.shortcuts import render


def process(request):
    return render(request, 'login_user.html')


def register(request):
    return render(request, 'reg.html')

