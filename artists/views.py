from django.shortcuts import render

from django.views.generic import ListView, DetailView

def artists_home(request):
    return render(
        request,
        'artists/index.html'
    )

