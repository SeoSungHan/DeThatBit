from django.shortcuts import render, redirect
from django.contrib.auth import login as user_login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserForm
from albums.models import Albums
from review_board.models import Review_Post
from free_board.models import Free_Post

from django.views.decorators.http import require_http_methods
from django.contrib import messages
# Create your views here.


def landing(request):
    recent_album = Albums.objects.all().order_by('-date')[0:6]
    recent_review = Review_Post.objects.all().order_by('-pk')[0:10]
    recent_free = Free_Post.objects.all().order_by('-pk')[0:10]
    return render(
        request,
        'single_pages/landing.html',
        {'album': recent_album,
         'review': recent_review,
         'free': recent_free}
    )


def about_this(request):
    return render(
        request,
        'single_pages/about_this.html'
    )


def sign_up(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():  # 회원가입 폼에서 적어 보낸 요청이 유효한지 검사한다.
            # 유효한 내용이면 이 회원 정보를 데이터베이스에 저장한다. 그 유저 정보를 리턴한다.
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            user_login(request, user)  # 유저 정보를 이용해 로그인한다.
            return redirect('single_pages:landing')
        # redirect 시 urls.py의 <app_name>:<name>으로 요청을 보낸다.
        else:
            messages.error(request, form.errors)
            #redirect('/')
    else:
        form = UserCreationForm()  # 비어있는 회원가입 폼을 생성한다.
    return render(request, 'single_pages/sign_up.html', {'form': form})
    # forms.html 파일을 렌더한다. 이때 위에서 생성한 회원가입 폼을 'form'이라는 이름으로 함께 보낸다.(딕셔너리)
