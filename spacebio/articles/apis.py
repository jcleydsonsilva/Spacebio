import requests
from django.core.cache import cache

def get_spaceflight_news():
    cached_data = cache.get('spaceflight_news')
    if cached_data:
        return cached_data
    else:
        url = "https://api.spaceflightnewsapi.net/v4/articles"
        response = requests.get(url)
        space_news = response.json()
        cache.set('spaceflight_news', space_news, timeout=(60 * 10))
        print("Dados armazenados no cache:", space_news)  # Para fins de debug
        return space_news


def get_spacelaunchs():
    cached_data = cache.get('spacelaunchs')
    if cached_data:
        return cached_data
    else:
        url = "https://lldev.thespacedevs.com/2.2.0/launch/upcoming"
        response = requests.get(url, params={'limit': 4})
        spacelaunchs = response.json()
        cache.set('spacelaunchs', spacelaunchs, timeout=(60*10))
        return spacelaunchs
