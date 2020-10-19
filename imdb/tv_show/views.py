from django.shortcuts import render

def process (request):
    return render(request, 'tv_show.html')

