from django.shortcuts import render, redirect
from django.contrib.auth import login as user_login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def landing(request):
    return render(
        request,
        'single_pages/landing.html'
    )

def about_this(request):
    return render(
        request,
        'single_pages/about_this.html'
    )

def login(request):
    return render(
        request,
        'single_pages/login.html'
    )

def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid(): # 회원가입 폼에서 적어 보낸 요청이 유효한지 검사한다.
            user = form.save() # 유효한 내용이면 이 회원 정보를 데이터베이스에 저장한다. 그 유저 정보를 리턴한다.
            #user_login(request, user) # 유저 정보를 이용해 로그인한다.
        return redirect('single_pages:sign_up')
    	# redirect 시 urls.py의 <app_name>:<name>으로 요청을 보낸다.
    else:
        form = UserCreationForm() # 비어있는 회원가입 폼을 생성한다.
        return render(request, 'single_pages/sign_up.html', {'form': form})
    	# forms.html 파일을 렌더한다. 이때 위에서 생성한 회원가입 폼을 'form'이라는 이름으로 함께 보낸다.(딕셔너리)