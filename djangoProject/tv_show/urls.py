from django.urls import path

from . import views

urlpatterns = [
    path('', views.process, name='process'),
    path('<int:show_id>/', views.detail, name='detail'),
    path('<int:show_id>/<int:season_no>/', views.season_list, name='season_list'),
    path('<int:show_id>/<int:season_no>/<int:episode_no>/', views.episode_detail, name='episode_detail'),
    path('<int:show_id>/rating/', views.submit_rating, name='submit_rating'),
    path('<int:show_id>/<int:season_no>/<int:episode_no>/rating/', views.episode_rating, name='episode_rating'),
    path('<int:show_id>/<int:season_no>/<int:episode_no>/review/', views.episode_review, name='episode_review'),
    path('<int:show_id>/review/', views.submit_review, name='submit_review'),
    path('<int:show_id>/add_to_watchlist/', views.add_to_watchlist, name='add_to_watchlist'),
    path('<int:show_id>/remove_from_watchlist/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('sorted/', views.sort_list, name='sort_list'),
    path('<int:show_id>/season_select/', views.select_season_list, name='select_season_list')
]
