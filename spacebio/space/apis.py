import requests
from django.core.cache import cache
from django.utils.timezone import now
from .models import *


# gets data from api
def get_spacelaunches():
    cached_data = cache.get('spacelaunches')
    if cached_data:
        return cached_data
    else:
        url = "https://lldev.thespacedevs.com/2.2.0/launch/upcoming"
        response = requests.get(url, params={'limit': 8})
        spacelaunches = response.json
        cache.set('spacelaunchs', spacelaunches, timeout=(60*10))
        return spacelaunches

def get_nextspacelaunch():
    cached_data = cache.get('nextspacelaunch')
    if cached_data:
        return cached_data
    else:
        url = "https://lldev.thespacedevs.com/2.2.0/launch/upcoming"
        response = requests.get(url, params={'limit': 2})
        nextspacelaunch = response.json()
        cache.set('nextspacelaunchs', nextspacelaunch, timeout=(60*10))
        return nextspacelaunch
    
    
# gets data from database
def fecth_spacelaunchs(limit=None):
    current_time = now()
    nextspacelaunch = Launch.objects.filter(net__gte=current_time).order_by('net')
    
    if limit is not None:
        nextspacelaunch = nextspacelaunch[:limit]
        
    return nextspacelaunch

def fetch_spacenews(limit=None):
    spacenews = News.objects.all().order_by('-published_at')
    
    if limit is not None:
        spacenews = spacenews[:limit]
        
    return spacenews