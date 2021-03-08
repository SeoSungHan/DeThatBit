from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Review_Post

class Review_List(ListView):
    model = Review_Post
    template_name = 'review_board/list.html'
    ordering = '-pk'


class Review_Detail(DetailView):
    model = Review_Post
    template_name = 'review_board/detail.html'