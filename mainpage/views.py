import json
from pathlib import Path

from django.utils import timezone
from django.shortcuts import render

from accounts.models import Userinfo
from board.models import Stores
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from mainpage.models import traditional_market


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

    # 받은 parameter의 종류가 POST인 경우만 데이터를 넘겨줌
    if request.method == 'POST': 
        request.session['marketNum'] = request.POST['selectMarket'] 
        request.session['selectMarketName'] = request.POST['selectMarketName'] 
        request.session['selectMarketAddress'] = request.POST['selectMarketAddress'] 

    if request.session.get('marketNum') is not None: # 시장 세션값이 존재하면
        marketNum = request.session['marketNum']
        selectMarketName = request.session['selectMarketName'] 
        selectMarketAddress =  request.session['selectMarketAddress']
        data = { 
            'marketNum' : marketNum, 
            'selectMarketName' : selectMarketName, 
            'selectMarketAddress' : selectMarketAddress
        }
        return render(request, 'mainpage/main.html', data)
    else:
        return render(request, 'mainpage/main.html')


def storepage(request):
    return render(request, 'mainpage/store.html')

def storepage(request, item):
    stores = Stores.objects.filter()
    data = {
        'stores' : stores,
        'item' : item
    }
    return render(request, 'mainpage/store.html', data)

def makestore(request):
    traditional_markets = traditional_market.objects.filter(

    ).values('id', 'name', 'road_address', 'latitude', 'longitude')
    context = {'traditional_markets':traditional_markets}
    return render(request, 'mainpage/makestore.html', context)

def map(request):
    traditional_markets = traditional_market.objects.filter(

    ).values('id', 'name', 'road_address', 'latitude', 'longitude')
    context = {'traditional_markets':traditional_markets}
    return render(request, 'mainpage/map.html', context)

def storeInfo(request):
    if(request.method == 'POST'):
        stores = Stores()
        stores.owner = Userinfo.objects.get(id=int(request.POST['owner']))
        stores.name = request.POST['name']
        stores.category = request.POST['category']
        stores.address = request.POST['address'] + '(' + request.POST['addressSub'] + ')'
        
        #post.user = request.user
        stores.mainimage = request.FILES['imgs']
            
        #stores.phone 
        stores.date_joined = timezone.datetime.now()
        # 데이터베이스에 저장
        stores.save()
        print(stores.id)
        return render(request, 'mainpage/main.html')
        # return redirect('/detail/' + str(stores.id))
    else:
        return render(request, 'mainpage/store_info.html')

def mypage(request):
    return render(request, 'mainpage/main.html')

def store(request):
    return render(request, 'mainpage/single.html')

def dbupload(request):
    BASE_DIR = Path(__file__).resolve().parent.parent
    data = json.loads(open(BASE_DIR / 'data.json', encoding='UTF8').read())
    name = data['records']
    num = 0
    for i in name:
        num = num + 1
        traditional_market.objects.create(
            name = i['시장명'],
            market_type = i['시장유형'],
            road_address = i['소재지도로명주소'],
            number_address = i['소재지지번주소'],
            latitude = i['위도'] if i['위도'] != '' else 0,
            longitude = i['경도'] if i['경도'] != '' else 0,
            handling_item = i['취급품목'] if "취급품목" in i else 'None', 
            opening_year = i['개설연도'],
            phone_number = i['전화번호'] if "전화번호" in i else 'None',
        ).save()
    return render(request, 'accounts/dbupload.html')