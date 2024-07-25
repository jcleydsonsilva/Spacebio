from .models import SpaceExploration

def recent_articles(request):
    recent_articles = SpaceExploration.objects.all().order_by('-id')[:5]
    
    return {'recent_articles': recent_articles}
