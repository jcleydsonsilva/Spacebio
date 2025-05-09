"""
URL configuration for spacebio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path

from articles import (
    views as articles_views,    
)
from space import (
    views as space_views,
)

DJANGO_PATHS = [
    path("admin/", admin.site.urls, name='admin:index'),
]


ARTICLES_PATHS = [
    path('', articles_views.home, name='home'),
    path('articles/list', articles_views.article_list, name='articles'),
    path('space_literature', articles_views.space_literature, name='space_literature'),
    path('team/', articles_views.team_view, name='team_view'),
    path('timeline/', articles_views.timeline_view, name='timeline_view'),
    path('getInvolved/', articles_views.getInvolved_view, name='getInvolved_view'),
    path('spacebio_lab/', articles_views.spacebio_lab_view, name='spacebio_lab_view'),
    
]

SPACE_PATHS = [
    path('launches', space_views.launches, name="launches"),
    path('news', space_views.news, name="news"),
    path('space/launch/<str:launch_id>', space_views.launch, name="launch"),
    path('spacebiotv/', space_views.spacebiotv_view, name='spacebiotv_view'),
    path('stellarium/', space_views.stellarium_view, name='stellarium_view'),
]

urlpatterns = DJANGO_PATHS + ARTICLES_PATHS + SPACE_PATHS