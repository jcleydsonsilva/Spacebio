from django.shortcuts import render
from django.http import HttpResponse

from articles.models import SpaceExploration


def home(request):
    return render(request, 'articles/home.html')
