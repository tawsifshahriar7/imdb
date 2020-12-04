from django.urls import path

from . import views

urlpatterns = [
    path('', views.process, name='process'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('add_tvshow/', views.add_tvshow, name='add_tvshow'),
    path('add_celeb/', views.add_celeb, name='add_celeb'),
    path('movie_added/', views.movie_added, name='movie_added'),
    path('show_added/', views.show_added, name='show_added'),
    path('celeb_added/', views.celeb_added, name='celeb_added'),
    path('add_episode/', views.add_episode, name='add_episode'),
    path('episode_added/', views.episode_added, name='episode_added'),
]