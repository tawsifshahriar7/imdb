from django.urls import path

from . import views

urlpatterns = [
    path('', views.process, name='process'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('movie_added/', views.movie_added, name='movie_added'),
]