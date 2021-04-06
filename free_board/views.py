import json
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from .models import Free_Post, Free_Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q

class Free_List(ListView):
    model = Free_Post
    template_name = 'free_board/list.html'
    ordering = '-pk'
    paginate_by=10

    def get_context_data(self, **kwargs):
        context = super(Free_List, self).get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5  # Display only 5 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        context['start_page'] = start_index
        context['last_page']=end_index
        return context

class Free_Search(Free_List):
    paginate_by=10

    def get_queryset(self):
        q=self.kwargs['q']
        t=int(self.kwargs['type'])

        if t==1:
            free_list=Free_Post.objects.filter(
                Q(title__contains=q)
            ).distinct()
        elif t==2:
            free_list=Free_Post.objects.filter(
                Q(content__contains=q)
            ).distinct()
        elif t==3:
            free_list=Free_Post.objects.filter(
                Q(author__username__contains=q)
            ).distinct()
        return free_list

    def get_context_data(self,**kwargs):
        context=super(Free_Search,self).get_context_data()
        q=self.kwargs['q']
        context['search_info']=f'Search: {q} ({self.get_queryset().count()})'
        
        return context

class Free_Detail(DetailView):
    model = Free_Post
    template_name = 'free_board/detail.html'
    
    def get_context_data(self, **kwargs):
       context=super(Free_Detail, self).get_context_data()
       context['comment_form']=CommentForm
       return context

@login_required
def Free_Post_Like(request):
    pk=request.POST.get('pk',None)
    post=get_object_or_404(Free_Post, pk=pk)
    user=request.user

    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
        message="좋아요 취소"
    else:
        post.likes.add(user)
        message="좋아요"

    context={'likes_cnt':post.get_likes_num(),'message':message}

    return HttpResponse(json.dumps(context), content_type="application/json")

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
def Free_Comment_Update(request, pk):
    comment=get_object_or_404(Free_Comment, pk=pk)
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