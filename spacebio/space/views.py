import os
from datetime import datetime, timezone
# Get the directory path of the current file (views.py)
current_directory = os.path.dirname(os.path.abspath(__file__))
# Define the path to the file within app directory
file_path = os.path.join(current_directory, 'inputs.txt')

from django.core.cache import cache
from django.shortcuts import render
from django.utils.timezone import now
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_filters.views import FilterView

from articles.models import SpaceExploration
from space.models import *
from space.apis import fecth_spacelaunchs, fetch_spacenews
from django.templatetags.static import static

from space.filters_launch import LaunchFilter
from space.filters_video import VideoFilter


def launches(request):
    current_time = now()

    # Create a blank filter first, as it will be applied to each QuerySet
    all_launches = Launch.objects.all()
    launch_filter = LaunchFilter(request.GET, queryset=all_launches)

    # Upcoming or current launches, ordered by ascending window_start
    upcoming_launches = launch_filter.qs.filter(window_start__gte=current_time).order_by('window_start')

    # Past launches, ordered by descending window_end
    past_launches = launch_filter.qs.filter(window_start__lt=current_time).order_by('-window_end')

    # Combine both QuerySets using union()
    # launches = upcoming_launches.union(past_launches)
    launches = upcoming_launches

    # Debug: print query to check applied filters
    print(launches.query)

    # Create a paginator for the launches
    launches_paginator = Paginator(launches, 16)
    page_number = request.GET.get('page')

    try:
        # Get the launches for the requested page
        launches = launches_paginator.page(page_number)
    except PageNotAnInteger:
        # If page number is not an integer, deliver first page.
        launches = launches_paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        launches = launches_paginator.page(launches_paginator.num_pages)

    return render(request, 'space/launches.html', {'launches': launches, 'filter': launch_filter})



def launch(request, launch_id):
    launch = Launch.objects.get(id=launch_id)
    
    return render(request, 'space/launch.html', {'launch': launch})



def news(request):
    # Fetch space news from the database
    space_news = fetch_spacenews()
    
    #create a paginator for the news
    news_paginator = Paginator(space_news, 24)
    
    # Get the page number from the request
    page_number = request.GET.get('page')
    
    try:
        # Get the news for the requested page
        space_news = news_paginator.page(page_number)
    except PageNotAnInteger:
        # If page number is not an integer, deliver first page.
        space_news = news_paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        space_news = news_paginator.page(news_paginator.num_pages)
    
    return render(request, 'space/news.html', {'space_news': space_news})



def spacebiotv_view(request):
    query = request.GET.get('search')
    filter_type = request.GET.get('filter')
    videos = VidURLs.objects.all().filter(url__contains="youtube.com").order_by('-id')
    
    if filter_type:
        if filter_type == 'videos':
            videos = videos.filter(~Q(title__icontains='live'))
        elif filter_type == 'live':
            videos = videos.filter(title__contains='live')
        elif filter_type == 'all':
            pass  # Mostrar todos os vídeos
    
    if query:
        videos = videos.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(publisher__icontains=query)
        )

    
    #create a paginator for the news
    videos_paginator = Paginator(videos, 15)
    
    # Get the page number from the request
    page_number = request.GET.get('page')
    
    try:
        # Get the news for the requested page
        videos = videos_paginator.page(page_number)
    except PageNotAnInteger:
        # If page number is not an integer, deliver first page.
        videos = videos_paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        videos = videos_paginator.page(videos_paginator.num_pages)
        
        
    context = {
        'videos': videos,
        'query': query,
        'filter_type': filter_type,
    }
    return render(request, 'space/spacebiotv.html', context)


def stellarium_view(request):
    return render(request, 'space/stellarium.html')
