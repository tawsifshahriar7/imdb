from django.shortcuts import render
from django.db import connection

def process (request):
    return render(request, 'index.html')

