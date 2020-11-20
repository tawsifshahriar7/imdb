from django.urls import path

from . import views

urlpatterns = [
    path('', views.process, name='process'),
    path('logout/', views.logout, name='logout'),
]
