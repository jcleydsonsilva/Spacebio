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
from django.urls import path

from articles import (
    views as articles_views,    
)

from dashboard import (
    views as dashboard_views,
)

DJANGO_PATHS = [
    path("admin/", admin.site.urls, name='admin:index'),
]


DASHBOARD_PATHS = [
    path('dashboard', dashboard_views.dashboard, name='dashboard'),
    path('dashboard/profile', dashboard_views.profile, name='dashboard/profile'),
    path('dashboard/calendar', dashboard_views.calendar, name='dashboard/calendar'),
    path('dashboard/form-elements', dashboard_views.formElements, name='dashboard/form-elements'),
    path('dashboard/form-layout', dashboard_views.formLayout, name='dashboard/form-layout'),

]


ARTICLES_PATHS = [
    path('', articles_views.home, name='home'),

]


urlpatterns = DJANGO_PATHS + DASHBOARD_PATHS + ARTICLES_PATHS