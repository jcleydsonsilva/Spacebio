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

from dashboard import (
    views as dashboard_views,
)

DJANGO_PATHS = [
    path("admin/", admin.site.urls, name='admin:index'),
]


ARTICLES_PATHS = [
    path('', articles_views.home, name='home'),
    path('articles/list', articles_views.article_list, name='articles'),
    path('articles/main', articles_views.article_main, name="main")
]




DASHBOARD_PATHS = [
    path('dashboard', dashboard_views.dashboard, name='dashboard'),
    path('dashboard/profile', dashboard_views.profile, name='dashboard/profile'),
    path('dashboard/calendar', dashboard_views.calendar, name='dashboard/calendar'),
    path('dashboard/form-elements', dashboard_views.formElements, name='dashboard/form-elements'),
    path('dashboard/form-layout', dashboard_views.formLayout, name='dashboard/form-layout'),
    path('dashboard/tables', dashboard_views.tables, name='dashboard/tables'),
    path('dashboard/settings', dashboard_views.settings, name='dashboard/settings'),
    path('dashboard/chart', dashboard_views.chart, name='dashboard/chart'),
    path('dashboard/alerts', dashboard_views.alerts, name='dashboard/alerts'),
    path('dashboard/buttons', dashboard_views.buttons, name='dashboard/buttons'),
    path('dashboard/signin', dashboard_views.signIn, name ='dashboard/signin'),
    path('dashboard/signup', dashboard_views.signUp, name='dashboard/signup')
]




urlpatterns = DJANGO_PATHS + ARTICLES_PATHS + DASHBOARD_PATHS 