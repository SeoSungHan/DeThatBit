import json
import math
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import Review_Post, Review_Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from albums.models import Albums
from django.db.models import Q
from django.contrib import messages

class Review_List(ListView):
    model = Review_Post
    template_name = 'review_board/list.html'
    ordering = '-pk'
    paginate_by=10

    def get_context_data(self, **kwargs):
        context = super(Review_List, self).get_context_data(**kwargs)
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

class Review_Search(Review_List):
    paginate_by=10

    def get_queryset(self):
        q=self.kwargs['q']
        t=int(self.kwargs['type'])

        if t==1:
            review_list=Review_Post.objects.filter(
                Q(title__contains=q)
            ).distinct()
        elif t==2:
            review_list=Review_Post.objects.filter(
                Q(content__contains=q)
            ).distinct()
        elif t==3:
            review_list=Review_Post.objects.filter(
                Q(author__username__contains=q)
            ).distinct()
        elif t==4:
            review_list=Review_Post.objects.filter(
                Q(album__album__contains=q)
            ).distinct()
        return review_list

    def get_context_data(self,**kwargs):
        context=super(Review_Search,self).get_context_data()
        q=self.kwargs['q']
        context['search_info']=f'Search: {q} ({self.get_queryset().count()})'
        
        return context

class Review_Detail(DetailView):
    model = Review_Post
    template_name = 'review_board/detail.html'

    def get_context_data(self, **kwargs):
       context=super(Review_Detail, self).get_context_data()
       context['comment_form']=CommentForm
       return context

def Album_Select(request):
    word=request.POST.get('q',None)
    if word:
        results=Albums.objects.filter(Q(album__contains=word)).distinct()

        limit=len(results)
        if limit>5: limit=5

        album_select=""
        
        for i in range(limit):
            if i==limit-1:album_select+=results[i].album
            else:album_select+=results[i].album + '\n'

        context={'album_select':album_select}
        return HttpResponse(json.dumps(context), content_type="application/json")

@login_required
def Review_Post_Like(request):
    pk=request.POST.get('pk',None)
    post=get_object_or_404(Review_Post, pk=pk)
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
def Review_Post_Like(request):
    pk=request.POST.get('pk',None)
    post=get_object_or_404(Review_Post, pk=pk)
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
def Review_Post_Create(request):
    if request.method == "POST":
        album = request.POST.get('album',None)
        rating_tmp=request.POST.get('rating',None)
        form = PostForm(request.POST)
        if not rating_tmp:
            return render(request, 'review_board/edit.html', {'form': form, 'rating_error':True, 'album':album})
        rating = float(rating_tmp)/2.
        if album:
            result=Albums.objects.filter(Q(album=album))
            if result and form.is_valid():
                post = form.save(commit=False)
                post.album = result[0]
                post.author = request.user
                post.rating = rating
                post.save()
                album=post.album
                album.rating=album.rating*album.reviews + post.rating
                album.reviews+=1
                album.rating/=album.reviews
                album.save()
                return redirect('../', pk=post.pk)
            else:
                return render(request, 'review_board/edit.html', {'form': form, 'album_error':True, 'album':album })
        else: 
            return render(request, 'review_board/edit.html', {'form': form, 'album_error':True })
    else:
        form = PostForm()
        return render(request, 'review_board/edit.html', {'form': form})

@login_required
def Review_Post_Update(request, pk):
    post = get_object_or_404(Review_Post, pk=pk)
    if request.user==post.author:
    
        if request.method == "POST":
            #우선 여기서 리뷰가 있기전 상태로 만듬
            album=post.album
            album.rating=album.rating*album.reviews-post.rating
            album.reviews-=1
            if album.reviews==0: album.rating=0
            else: album.rating/=album.reviews
            album.save()
            #여기까진 잘 작동함

            album = request.POST.get('album',None)
            rating_tmp = request.POST.get('rating',None)

            form = PostForm(request.POST, instance=post)
            rating=float(rating_tmp)/2.

            if album:
                #form = PostForm(request.POST, instance=post)
                result=Albums.objects.filter(Q(album=album))
                if result and form.is_valid():
                    post = form.save(commit=False)
                    post.album = result[0]
                    post.author = request.user
                    post.rating = rating
                    post.save()
                    album=post.album
                    album.rating=album.rating*album.reviews+post.rating
                    album.reviews+=1
                    album.rating/=album.reviews
                    album.save()
                    return redirect('../', pk=post.pk)
                else: 
                    return render(request, 'review_board/edit.html', {'rating':round(post.rating,2), 'album':post.album.album,'form': form, 'album_error':True})
            else:
                return render(request, 'review_board/edit.html', {'rating':round(post.rating,2), 'album':post.album.album,'form': form, 'album_error': True})        
        else:
            form = PostForm(instance=post)
            return render(request, 'review_board/edit.html', {'rating':round(post.rating,2), 'album':post.album.album,'form': form})
    else: return redirect('../')

@login_required
def Review_Post_Delete(request, pk):
    post = Review_Post.objects.get(pk=pk)
    if request.user==post.author:
        album=post.album
        album.rating=album.rating*album.reviews - post.rating
        album.reviews-=1
        album.rating/=album.reviews
        album.save()
        post.delete()
        return redirect('../../')
    else:
        return redirect('../')

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
