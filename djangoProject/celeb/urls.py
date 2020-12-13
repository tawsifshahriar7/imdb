from django.urls import path

from . import views

urlpatterns = [
    path('', views.process, name='process'),
    path('<int:celeb_id>/', views.detail, name='detail'),
    path('<int:celeb_id>/<int:show_id>/<str:role>/', views.celeb_ep_list, name='celeb_ep_list'),
]
