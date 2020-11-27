from django.urls import path

from . import views

urlpatterns = [
    path('', views.process, name='process'),
    path('<int:show_id>/', views.detail, name='detail'),
    path('<int:show_id>/review/', views.submit_review, name='submit_review'),
]