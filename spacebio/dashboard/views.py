from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def dashboard(request):
    page = 'ecommerce'
    return render(request, 'dashboard/index.html', {'page' : page})

@login_required(login_url="signin")
def profile(request):
    page = 'profile'
    return render(request, 'dashboard/profile.html', {'page' : page})

def calendar(request):
    page = 'calendar'
    return render(request, 'dashboard/calendar.html', {'page' : page})

def formElements(request):
    page = 'formElements'
    return render(request, 'dashboard/form-elements.html', {'page' : page})

def formLayout(request):
    page = 'formLayout'
    return render(request, 'dashboard/form-layout.html', {'page' : page})

def tables(request):
    page = 'tables'
    return render(request, 'dashboard/tables.html', {'page' : page})

def settings(request):
    page = 'settings'
    return render(request, 'dashboard/settings.html', {'page' : page})

def chart(request):
    page = 'chart'
    return render(request, 'dashboard/chart.html', {'page' : page})

def alerts(request):
    page = 'alerts'
    return render(request, 'dashboard/alerts.html', {'page' : page})

def buttons(request):
    page = 'buttons'
    return render(request, 'dashboard/buttons.html', {'page' : page})

def signIn(request):
    page = 'signin'
    return render(request, 'dashboard/signin.html', {'page' : page})

def signUp(request):
    page = 'signup'
    return render(request, 'dashboard/signup.html', {'page' : page})