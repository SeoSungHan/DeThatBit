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
    
    def get_context_data(self, **kwargs):
       context=super(Free_Detail, self).get_context_data()
       context['comment_form']=CommentForm
       return context

@login_required
def Free_Comment_Create(request, pk):
    post=get_object_or_404(Free_Post, pk=pk)

    if request.method == 'POST':
                comment_form=CommentForm(request.POST)
                if comment_form.is_valid():
                    comment=comment_form.save(commit=False)
                    comment.free_post=post
                    comment.writer=request.user
                    comment.save()
                    return redirect(comment.get_absolute_url())
    else :
                return redirect(post.get_free_url())

@login_required
def Free_Comment_Delete(request, pk):
    comment=get_object_or_404(Free_Comment, pk=pk)
    post=comment.free_post
    if request.user==comment.writer:
        comment.delete()
        return redirect(post.get_free_url())
    else:
        return redirect(comment.get_absolute_url())

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