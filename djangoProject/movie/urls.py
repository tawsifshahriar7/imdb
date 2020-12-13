from django.urls import path

from . import views

urlpatterns = [
    path('', views.process, name='process'),
    path('<int:movie_id>/', views.detail, name='detail'),
    path('<int:movie_id>/rating/', views.submit_rating, name='submit_rating'),
    path('<int:movie_id>/review/', views.submit_review, name='submit_review'),
    path('<int:movie_id>/add_to_watchlist/', views.add_to_watchlist, name='add_to_watchlist'),
    path('<int:movie_id>/remove_from_watchlist/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('sorted/', views.sort_list, name='sort_list')
]
