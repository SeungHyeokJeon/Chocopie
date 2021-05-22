import json
from django.shortcuts import render
from mainpage.models import Userinfo, SocialaccountSocialaccount, AuthUser

# Create your views here.
def mainpage(request):
    authId = request.session.get('_auth_user_id')
    
    if authId!='' and authId!=None: # 로그인된 계정이 존재하면
        # 로그인계정의 회원정보가 등록되어있는지 판단
        existId = Userinfo.objects.filter(id=int(authId))
        #existId = Userinfo.objects.all()
        if len(existId)==0:
            # 등록이 안되어 있으면 넘겨줄 값들을 하나씩 불러옴
            # 넘겨주는 값: auth_user.id, provider, name
            socialAccount = SocialaccountSocialaccount.objects.filter(user_id=authId)
            extraData = json.loads(socialAccount[0].extra_data)
            provider = socialAccount[0].provider # provider
            if provider=='kakao': # provider가 kakao면 nickname으로 name 가져옴
                name = extraData['properties']['nickname']
            else: # provider가 google이나 naver면 name으로 가져옴
                name = extraData['name']

            context={'authid':authId, 'provider':provider,'name':name}
            return render(request, 'accounts/additionalRegister.html',context)
            
    return render(request, 'mainpage/main.html')