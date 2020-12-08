from django.urls import path

from . import views

urlpatterns = [
    path('', views.process, name='process'),
    path('logout/', views.logout, name='logout'),
    path('id=<str:handle>/', views.public, name='public'),
    path('id=<str:handle>/change_picture/', views.change_dp, name='change_dp'),
    path('id=<str:handle>/dp_changed/', views.dp_changed, name='dp_changed'),
    path('id=<str:handle>/change_password/', views.change_pass, name='change_pass'),
    path('id=<str:handle>/pass_changed/', views.pass_changed, name='pass_changed'),
]
