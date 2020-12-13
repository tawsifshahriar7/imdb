from django.urls import path

from . import views

urlpatterns = [
    path('', views.process, name='process'),
    path('upload/', views.upload, name='upload'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout, name='logout'),
    path('id=<str:handle>/', views.public, name='public'),
    path('<int:show_id>/', views.episode_section, name='episode_section'),
]
