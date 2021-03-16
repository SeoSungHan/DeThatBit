from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Albums

class Albums_List(ListView):
    model = Albums
    template_name = 'albums/index.html'
    ordering = '-pk'
    paginate_by=20

