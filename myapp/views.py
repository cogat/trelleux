from django.http import Http404
from django.shortcuts import render

def dashboard(request):
    context = {}
    return render(request, 'dashboard.html', context)
