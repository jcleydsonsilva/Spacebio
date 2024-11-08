from .models import Article

def recent_articles(request):
    recent_articles = Article.objects.filter(doi__contains='/', journal_year_of_publication__gte=2024)[:5]
    
    return {'recent_articles': recent_articles}
