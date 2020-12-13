"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('djangoProject.index.urls')),
    path('login/', include('djangoProject.loginUser.urls')),
    path('movie/', include('djangoProject.movie.urls')),
    path('tvshow/', include('djangoProject.tv_show.urls')),
    path('profile/', include('djangoProject.profile_user.urls')),
    path('search/', include('djangoProject.search.urls')),
    path('celeb/', include('djangoProject.celeb.urls')),
    path('superuser/', include('djangoProject.superuser.urls')),
    path('news/', include('djangoProject.news.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
