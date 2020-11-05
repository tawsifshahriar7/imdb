from django.urls import path

from . import views

urlpatterns = [
    path('', views.process, name='process'),
    path('<int:movie_id>/', views.detail, name='detail'),
]