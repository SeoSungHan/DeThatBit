from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import Review_Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required

class Review_List(ListView):
    model = Review_Post
    template_name = 'review_board/list.html'
    ordering = '-pk'


class Review_Detail(DetailView):
    model = Review_Post
    template_name = 'review_board/detail.html'

@login_required
def Review_Post_Create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('../', pk=post.pk)
    else:
        form = PostForm()
        return render(request, 'review_board/edit.html', {'form': form})

@login_required
def Review_Post_Update(request, pk):
    post = get_object_or_404(Review_Post, pk=pk)
    if request.user==post.author:
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('../', pk=post.pk)
        else:
            form = PostForm(instance=post)
            return render(request, 'review_board/edit.html', {'form': form})
    else: return redirect('../')

@login_required
def Review_Post_Delete(request, pk):
    post = Review_Post.objects.get(pk=pk)
    if request.user==post.author:
        post.delete()
        return redirect('../../')
    else:
        return redirect('../')