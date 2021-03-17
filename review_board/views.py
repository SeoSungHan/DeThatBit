from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import Review_Post, Review_Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

class Review_List(ListView):
    model = Review_Post
    template_name = 'review_board/list.html'
    ordering = '-pk'

class Review_Detail(DetailView):
    model = Review_Post
    template_name = 'review_board/detail.html'

    def get_context_data(self, **kwargs):
       context=super(Review_Detail, self).get_context_data()
       context['comment_form']=CommentForm
       return context

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
def Review_Comment_Create(request, pk):
    post=get_object_or_404(Review_Post, pk=pk)

    if request.method == 'POST':
                comment_form=CommentForm(request.POST)
                if comment_form.is_valid():
                    comment=comment_form.save(commit=False)
                    comment.review_post=post
                    comment.writer=request.user
                    comment.save()
                    return redirect(comment.get_absolute_url())
    else :
                return redirect(post.get_review_url())

@login_required
def Review_Comment_Update(request, pk):
    comment=get_object_or_404(Review_Comment, pk=pk)
    if request.user==comment.writer:
        if request.method == 'POST':
            comment_form=CommentForm(request.POST, instance=comment)
            if comment_form.is_valid():
                comment=comment_form.save(commit=False)
                comment.save()
                return redirect(comment.get_absolute_url())
        else :
            comment_form=CommentForm(instance=comment)
            return redirect(comment.get_absolute_url())
    else:
        return redirect(comment.get_absolute_url())

@login_required
def Review_Comment_Delete(request, pk):
    comment=get_object_or_404(Review_Comment, pk=pk)
    post=comment.review_post
    if request.user==comment.writer:
        comment.delete()
        return redirect(post.get_review_url())
    else:
        return redirect(comment.get_absolute_url())

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