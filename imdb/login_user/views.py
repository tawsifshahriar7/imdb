from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def process (request):
    return render(request, 'login_user.html')

