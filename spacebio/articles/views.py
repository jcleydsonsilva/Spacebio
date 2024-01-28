from django.views.generic import TemplateView

from articles.models import SpaceExploration

class ArticlesView(TemplateView):
    template_name = 'articles/articles.html'