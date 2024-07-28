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

from space.filters import LaunchFilter
 
def home(request):
    space_news = cache.get('space_news')
    
    articles_count = SpaceExploration.objects.all().count()
    recent_articles = SpaceExploration.objects.all().order_by('-id')[:5]

    nextspacelaunch = fecth_spacelaunchs(limit=2)
    space_news = fetch_spacenews(limit=10)
    
    return render(request, 'articles/home.html', {'space_news': space_news, 'nextspacelaunch': nextspacelaunch, 'articles_count': articles_count, 'recent_articles': recent_articles})

def space_literature(request):
    return render(request, 'articles/space_literature.html')

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


def launches(request):
    current_time = datetime.now().astimezone(timezone.utc)
    
    # Fetch space launches from the database
    launches = Launch.objects.all().order_by("-window_start")
    
    # Aplicar o filtro
    launch_filter = LaunchFilter(request.GET, queryset=launches)
    filtered_launches = launch_filter.qs
    
    # Debug: print query to check applied filters
    print(filtered_launches.query)
    
    # Create a paginator for the launches
    launches_paginator = Paginator(filtered_launches, 10)
    page_number = request.GET.get('page')
    
    try:
        # Get the launches for the requested page
        launches = launches_paginator.page(page_number)
    except PageNotAnInteger:
        # If page number is not an integer, deliver first page.
        launches = launches_paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        launches = launches_paginator.page(launches_paginator.num_pages)
    
    return render(request, 'articles/launches.html', {'launches': launches, 'filter': launch_filter})

def launch(request, launch_id):
    launch = Launch.objects.get(id=launch_id)
    
    return render(request, 'space/launch.html', {'launch': launch})

def news(request):
    # Fetch space news from the database
    space_news = fetch_spacenews()
    
    #create a paginator for the news
    news_paginator = Paginator(space_news, 10)
    
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
    
    return render(request, 'articles/news.html', {'space_news': space_news})


def stellarium_view(request):
    return render(request, 'articles/stellarium.html')

def team_view(request):

    collaborators = [
        {
            'name': 'Alice Smith',
            'role': 'Data Scientist',
            'bio': 'Alice is an experienced data scientist with a focus on machine learning and AI.',
            'image': 'https://via.placeholder.com/400',
        },
        {
            'name': 'Bob Johnson',
            'role': 'Backend Developer',
            'bio': 'Bob is a seasoned backend developer specializing in Django and REST APIs.',
            'image': 'https://via.placeholder.com/400',
        },
        {
            'name': 'Charlie Brown',
            'role': 'Frontend Developer',
            'bio': 'Charlie is a creative frontend developer with expertise in React and Tailwind CSS.',
            'image': 'https://via.placeholder.com/400',
        },
        # Adicione mais colaboradores conforme necessário
    ]
    return render(request, 'articles/team.html',{'collaborators': collaborators})

def timeline_view(request):
    return render(request, 'articles/timeline.html')

def getInvolved_view(request):
    return render(request, 'articles/getInvolved.html')

def spacebiotv_view(request):
    videos=[
        {'1':'https://www.youtube.com/watch?v=8sy2XXk_UwQ'},
        {'2':'https://www.youtube.com/watch?v=mhJRzQsLZGg'},
        {'4':'https://www.youtube.com/watch?v=21X5lGlDOfg'},
    ]
    return render(request, 'articles/spacebiotv.html',{'videos':videos})