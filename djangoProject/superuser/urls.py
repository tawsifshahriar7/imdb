from django.urls import path

from . import views

urlpatterns = [
    path('', views.process, name='process'),
    path('profile/', views.profile, name='profile'),
    path('movie_added/', views.movie_added, name='movie_added'),
    path('show_added/', views.show_added, name='show_added'),
    path('celeb_added/', views.celeb_added, name='celeb_added'),
    path('<int:show_id>/', views.new_season, name='new_season'),
    path('<int:show_id>/<int:season_no>/', views.new_episode, name='new_episode'),
    path('<int:show_id>/<int:season_no>/episode_added/', views.episode_added, name='episode_added'),
    path('<int:celeb_id>/celeb_edit/', views.celeb_update, name='celeb_update'),
    path('<int:celeb_id>/celeb_movie/', views.celeb_movie_update, name='celeb_movie_update'),
    path('<int:celeb_id>/celeb_show/', views.celeb_show_update, name='celeb_show_update'),
    path('<int:celeb_id>/celeb_episode/', views.celeb_ep_update, name='celeb_ep_update')
]
