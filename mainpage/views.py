import json
from django.shortcuts import render
from accounts.models import Userinfo
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress

# Create your views here.
def mainpage(request):
    authId = request.session.get('_auth_user_id')
    
    if authId!='' and authId!=None: # 로그인된 계정이 존재하면
        # 로그인계정의 회원정보가 등록되어있는지 판단
        existId = Userinfo.objects.filter(id=authId)
        if not existId.exists():
            # 등록이 안되어 있으면 넘겨줄 값들을 하나씩 불러옴
            # 넘겨주는 값: auth_user.id, provider, name
            socialAccountInfo = SocialAccount.objects.get(user_id=authId)
            
            provider = socialAccountInfo.provider # provider

            if provider=='kakao': # provider가 kakao면 nickname으로 name 가져옴
                name = socialAccountInfo.extra_data['properties']['nickname']
            else: # provider가 google이나 naver면 name으로 가져옴
                name = socialAccountInfo.extra_data['name']

            context={'authid':authId, 'provider':provider,'name':name}
            return render(request, 'accounts/additionalRegister.html',context)

    return render(request, 'mainpage/main.html')