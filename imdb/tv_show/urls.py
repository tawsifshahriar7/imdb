from django.urls import path

from . import views

urlpatterns = [
    path('', views.process, name='process'),
    path('<int:show_id>/', views.detail, name='detail'),
    path('<int:show_id>/review/', views.submit_review, name='submit_review'),
    path('<int:show_id>/add_to_watchlist/', views.add_to_watchlist, name='add_to_watchlist'),
    path('<int:show_id>/remove_from_watchlist/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('<int:show_id>/s<int:season_no>e<int:episode_no>/', views.episode_details, name= 'episode_details'),
    path('<int:show_id>/s<int:season_no>e<int:episode_no>/review/', views.episode_submit_review, name= 'episode_submit_review'),
]