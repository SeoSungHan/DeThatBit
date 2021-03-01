from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Free_Post

class Free_List(ListView):
    model=Free_Post
    template_name='free_board/list_example.html'
    ordering='-pk'

class Free_Detail(DetailView):
    model=Free_Post
    template_name='free_board/detail_example.html'
