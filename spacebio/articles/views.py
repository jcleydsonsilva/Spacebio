import os
from datetime import datetime, timezone, timedelta
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
 
def home(request):
    current_time = now()
    space_news = cache.get('space_news')
    
    articles_count = SpaceExploration.objects.all().count()
    recent_articles = SpaceExploration.objects.all().order_by('-id')[:5]

    nextspacelaunch = Launch.objects.filter(window_start__gte=current_time).order_by('window_start')[:2]
    space_news = fetch_spacenews(limit=10)
    
    return render(request, 'articles/home.html', {'space_news': space_news, 'nextspacelaunch': nextspacelaunch, 'articles_count': articles_count, 'recent_articles': recent_articles})

def space_literature(request):
    
    articles_count = SpaceExploration.objects.all().count()
    
    
    return render(request, 'articles/space_literature.html', {'articles_count': articles_count})

def article_list(request):
    query = request.GET.get('query')
    articles = []
    result_count = 0
    
    if query:
        keywords = [keyword.strip() for keyword in query.split()]
        
        query_filter = Q()
        for keyword in keywords:
            query_filter |= Q(title__icontains=keyword) | Q(abstract__icontains=keyword) | Q(authorstring__icontains=keyword)

        articles = SpaceExploration.objects.filter(query_filter)
        result_count = articles.count()

    articles_paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')

    try:
        articles = articles_paginator.page(page_number)
    except PageNotAnInteger:
        articles = articles_paginator.page(1)
    except EmptyPage:
        articles = articles_paginator.page(articles_paginator.num_pages)

    # Open or create the file for writing
    with open(file_path, 'a+') as file:
        # Write the user input to the file
        file.write(query + '\n')

    return render(request, 'articles/article_list.html', {'articles': articles, 'query': query, 'result_count': result_count})



def team_view(request):
    return render(request, 'articles/team.html')

def timeline_view(request):
    return render(request, 'articles/timeline.html')

def getInvolved_view(request):
    return render(request, 'articles/getInvolved.html')

