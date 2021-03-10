from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from .models import Free_Post, Free_Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
 
class Free_List(ListView):
    model = Free_Post
    template_name = 'free_board/list.html'
    ordering = '-pk'

class Free_Detail(DetailView):
    model = Free_Post
    template_name = 'free_board/detail.html'
    form_class=CommentForm
   
@login_required
def Free_Comment_Create(request, pk):
    if request.method == 'POST':
                comment = Free_Comment()
                comment.text = request.POST['text']
                comment.free_post = Free_Post.objects.get(pk=request.POST['free_post'])       
                comment.writer = request.user
                comment.save()
                return redirect('../')
    else :
                return redirect('../')

@login_required
def Free_Post_Create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('../', pk=post.pk)
    else:
        form = PostForm()
        return render(request, 'free_board/edit.html', {'form': form})

@login_required
def Free_Post_Update(request, pk):
    post = get_object_or_404(Free_Post, pk=pk)
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
            return render(request, 'free_board/edit.html', {'form': form})
    else: return redirect('../')

@login_required
def Free_Post_Delete(request, pk):
    post = Free_Post.objects.get(pk=pk)
    if request.user==post.author:
        post.delete()
        return redirect('../../')
    else:
        return redirect('../')