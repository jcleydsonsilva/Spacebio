from django.shortcuts import render
from django.http import HttpResponse


def dashboard(request):
    return render(request, 'dashboard/index.html')

def profile(request):
    return render(request, 'dashboard/profile.html')

def calendar(request):
    return render(request, 'dashboard/calendar.html')

def formElements(request):
    return render(request, 'dashboard/form-elements.html')

def formLayout(request):
    return render(request, 'dashboard/form-layout.html')