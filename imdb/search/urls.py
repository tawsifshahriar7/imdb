from django.urls import path

from . import views

urlpatterns = [
    path('', views.process, name='process'),
    path('result/', views.search, name= 'search'),
]