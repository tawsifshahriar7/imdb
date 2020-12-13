from django.urls import path

from . import views

urlpatterns = [
    path('', views.process, name='process'),
    path('register/', views.register, name='register'),
    path('auth/', views.login, name='login'),
    path('register/registration/', views.registration, name='registration'),
]
