from django.urls import path

from . import views

urlpatterns = [
    path('', views.process, name='process'),
    path('<int:show_id>/', views.detail, name='detail'),
    path('<int:show_id>/review/', views.submit_review, name='submit_review'),
    path('<int:show_id>/add_to_watchlist/', views.add_to_watchlist, name='add_to_watchlist'),
    path('<int:show_id>/remove_from_watchlist/', views.remove_from_watchlist, name='remove_from_watchlist'),
]