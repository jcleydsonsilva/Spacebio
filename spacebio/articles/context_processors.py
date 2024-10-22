from .models import Article

def recent_articles(request):
    recent_articles = Article.objects.all().order_by('-id')[:4]
    
    return {'recent_articles': recent_articles}
