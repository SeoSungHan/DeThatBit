from django.shortcuts import render
from django.views.generic import ListView, DetailView

def albums_home(request):
    return render(
        request,
        'albums/index.html'
    )

