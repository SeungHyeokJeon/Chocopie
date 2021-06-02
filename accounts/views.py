from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.models import Userinfo
from django.contrib.auth.models import User # auth_user
from allauth.socialaccount.models import SocialAccount, SocialToken
from allauth.account.models import EmailAddress
from django.contrib.sessions.models import Session

from datetime import datetime

# Create your views here.
def login(request):
    authId = request.session.get('_auth_user_id')
    dataList = User.objects.filter(id=authId)
    context = {'userData':dataList}
    return render(request, 'accounts/login.html',context)

def loginKakao(request):
    restApiKey = 'cc4da3338c1087e45c43b48a355072be'
    redirectUrl = 'http://127.0.0.1:8000/allauth/kakao/login/callback/'
    return redirect(f'https://kauth.kakao.com/oauth/authorize?client_id={restApiKey}&redirect_uri={redirectUrl}&response_type=code')

def withdrawal(request):
    return render(request, 'accounts/withdrawal.html')

def withdrawalProcess(request):
    authId = request.session.get('_auth_user_id')
    
    isDelete = request.POST.get('isdelete')
    isDelete='True'
    # 비정상 접근 막기
    if isDelete=='True':
        # 데이터가 삭제될 테이블: socialaccount_socialaccount, socialaccount_socialtoken, account_emailaddress, auth_user
        infoInstance = Userinfo.objects.filter(id=13)
        
        socialAccountInstance = SocialAccount.objects.get(user_id=authId)
        # token 삭제 위한 socialaccount id값
        socialAccountId = socialAccountInstance.id

        socialTokenInstance = SocialToken.objects.get(id=socialAccountId)
        emailAddressInstance = EmailAddress.objects.get(user_id=authId)
        userInstance = User.objects.get(id=authId)

        socialTokenInstance.delete()
        socialAccountInstance.delete()
        emailAddressInstance.delete()
        userInstance.delete()

        # 현재 세션 삭제
        request.session.flush()
    return redirect(reverse('mainpage:mainpage'))