import os
# Get the directory path of the current file (views.py)
current_directory = os.path.dirname(os.path.abspath(__file__))
# Define the path to the file within app directory
file_path = os.path.join(current_directory, 'inputs.txt')

from django.core.cache import cache
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from articles.models import SpaceExploration
from .apis import get_spaceflight_news, get_spacelaunchs
 
def home(request):
    page = 'ecommerce'

    # space_news = cache.get('space_news')
    # spacelaunchs = cache.get('spacelaunchs')
    # if space_news is None or spacelaunchs is None:
    #     space_news = get_spaceflight_news()
    #     spacelaunchs = get_spacelaunchs()
    #     cache.set('space_news', space_news, 60*10)  # 10 minutes
    #     cache.set('spacelaunchs', spacelaunchs, 60*10)

    return render(request, 'articles/home.html', {'page' : page})

def article_main(request):
    space_news = get_spaceflight_news()
    spacelaunchs = get_spacelaunchs()
    return render(request, 'articles/main.html', {'space_news': space_news, 'spacelaunchs': spacelaunchs})


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

    # Open or create the file for writing
    with open(file_path, 'a+') as file:
        # Write the user input to the file
        file.write(query + '\n')

    return render(request, 'articles/article_list.html', {'articles': articles, 'query': query, 'result_count': result_count})