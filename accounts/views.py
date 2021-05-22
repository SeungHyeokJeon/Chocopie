from django.shortcuts import render, redirect
from django.urls import reverse
from accounts.models import AuthUser, Userinfo
from datetime import datetime

# Create your views here.
def login(request):
    authId = request.session.get('_auth_user_id')
    dataList = AuthUser.objects.filter(id=authId)
    context = {'userData':dataList}
    return render(request, 'accounts/login.html',context)

def logout(request):
    return render(request, 'accounts/logout.html')

def loginKakao(request):
    restApiKey = 'cc4da3338c1087e45c43b48a355072be'
    redirectUrl = 'http://127.0.0.1:8000/allauth/kakao/login/callback/'
    return redirect(f'https://kauth.kakao.com/oauth/authorize?client_id={restApiKey}&redirect_uri={redirectUrl}&response_type=code')

def register(request):
    # 필요한 정보 받아오기
    authid = int(request.POST.get('authid'))
    provider = request.POST.get('provider')
    name = request.POST.get('name')
    email = request.POST.get('email')

    # 회원가입할 객체 생성하고 등록
    userInstance = Userinfo(id=AuthUser.objects.get(id=authid), provider=provider, name=name, email=email, date_joined=datetime.now())
    userInstance.save()

    return redirect(reverse('mainpage:mainpage'))