from django.shortcuts import render
from mainapp.rss_parser import get_trends
import time


def index(request):
    return render(request, 'mainapp/index.html', {'trends_112': get_trends()})