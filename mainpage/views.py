import json
from pathlib import Path
from datetime import datetime
import math

from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from accounts.models import Userinfo
from board.models import Stores, Boards
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from mainpage.models import traditional_market

from mainpage.forms import BoardsForm


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

            # 회원가입할 객체 생성하고 등록
            userInstance = Userinfo(id=User.objects.get(id=authId), provider=provider, name=name, date_joined=datetime.now())
            userInstance.save()

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
    marketNum = request.session['marketNum'] # 시장번호

    data = Stores.objects.filter(category=item, market_id=marketNum).order_by('id')

    listLength = 5  # 한번에 불러올 게시글 개수
    totalPage = math.ceil(len(data)/listLength) # 전체 페이지 계산

    paginator = Paginator(data,listLength) # 게시글 나누기
    page = request.GET.get('page') # page 파라미터 있으면 갖고오기
    
    try:
        store_list=paginator.page(page) # 현재 페이지 지정
    except PageNotAnInteger:
        store_list=paginator.page(1)
    except EmptyPage:
        store_list=paginator.page(paginator.num_pages)

    context = {
        'stores' : store_list,
        'totalPage':totalPage,
        'item' : item
    }
    return render(request, 'mainpage/store.html', context)

def makestore(request):
    marketNum = request.session['marketNum']
    selectMarketName = request.session['selectMarketName'] 
    selectMarketAddress =  request.session['selectMarketAddress']
    data = { 
        'marketNum' : marketNum,
        'selectMarketName' : selectMarketName, 
        'selectMarketAddress' : selectMarketAddress
    }
    return render(request, 'mainpage/makestore.html', data)

def storepage_ajax(request):
    item = request.POST.get('item')
    marketNum = request.session['marketNum'] # 시장번호

    data = Stores.objects.filter(category=item, market_id=marketNum).order_by('id')

    listLength = 5
    totalPage = math.ceil(len(data)/listLength)

    paginator = Paginator(data,listLength)
    page = request.POST.get('page')
    
    try:
        store_list = paginator.page(page)
    except PageNotAnInteger:
        store_list = paginator.page(1)
    except EmptyPage:
        store_list = paginator.page(paginator.num_pages)

    context = {
        'stores' : store_list,
        'totalPage':totalPage,
        'item' : item
    }
    return render(request, 'mainpage/store_list_ajax.html', context)

def makestore(request):
    traditional_markets = traditional_market.objects.filter(

    ).values('id', 'name', 'road_address', 'latitude', 'longitude')
    context = {'traditional_markets':traditional_markets}
    return render(request, 'mainpage/makestore.html', context)

def saveStore(request):
    if(request.method == 'POST'):
        stores = Stores()
        stores.owner = Userinfo.objects.get(id=int(request.POST['owner']))
        stores.market = Userinfo.objects.get(id=int(request.POST['marketNum']))

        stores.name = request.POST['name']
        stores.category = request.POST['category']
        stores.address = request.POST['address'] + '(' + request.POST['addressSub'] + ')'
        stores.introduce = request.POST['introduce']
        #post.user = request.user
        stores.mainimage = request.FILES['imgs']
            
        #stores.phone 
        stores.date_joined = timezone.datetime.now()
        # 데이터베이스에 저장
        stores.save()
        return redirect('/detail/' + str(stores.id))
    else:
        return redirect(reverse('mainpage:mainpage'))
    
def map(request):
    traditional_markets = traditional_market.objects.filter(

    ).values('id', 'name', 'road_address', 'latitude', 'longitude')
    context = {'traditional_markets':traditional_markets}
    return render(request, 'mainpage/map.html', context)

def detailStore(request, store_id):
    store = Stores.objects.get(id=int(store_id))
    owner = Userinfo.objects.get(id=int(store.owner_id))
    board = Boards.objects.filter(store=int(store_id)).order_by('-id')

    listLength = 5  # 한번에 불러올 게시글 개수
    totalPage = math.ceil(len(board)/listLength) # 전체 페이지 계산

    paginator = Paginator(board,listLength) # 게시글 나누기
    page = request.POST.get('page') # page 파라미터 있으면 갖고오기
    print('page:',page,'/',totalPage)
    
    try:
        board_list=paginator.page(page) # 현재 페이지 지정
    except PageNotAnInteger:
        board_list=paginator.page(1)
    except EmptyPage:
        board_list=paginator.page(paginator.num_pages)

    data = { 
        'store' : store,
        'owner' : owner,
        'board': board_list,
        'totalPage':totalPage
    }
    return render(request, 'mainpage/store_info.html', data)

def detailStore_ajax(request, id):
    board = Boards.objects.filter(store=id).order_by('id')

    listLength = 5  # 한번에 불러올 게시글 개수
    totalPage = math.ceil(len(board)/listLength) # 전체 페이지 계산

    paginator = Paginator(board,listLength) # 게시글 나누기
    page = request.POST.get('page') # page 파라미터 있으면 갖고오기
    print('ajax page:',page)
    
    try:
        board_list=paginator.page(page) # 현재 페이지 지정
    except PageNotAnInteger:
        board_list=paginator.page(1)
    except EmptyPage:
        board_list=paginator.page(paginator.num_pages)
    
    context = {
        'board': board_list,
        'totalPage':totalPage
    }
    return render(request, 'mainpage/board_ajax.html', context)


    
def mypage(request):
    return render(request, 'mainpage/mypage.html')

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

def post_write(request, store_id):
    authId = request.session.get('_auth_user_id')
    userinfo = Userinfo.objects.get(id=authId)
    store = Stores.objects.get(id=int(store_id))

    if request.method == "POST":
        form = BoardsForm(request.POST, request.FILES)
        if form.is_valid():
            post = Boards()
            post.store=store
            post.writer=userinfo
            post.writer_name=userinfo.name
            post.title = request.POST.get('title')
            post.content = request.POST.get('content')
            post.thumbnail = request.POST.get('thumbnail')
            post.views=0
            post.date_posted=timezone.datetime.now()
            post.save()
            return redirect(reverse('mainpage:detailStore', kwargs={'store_id':store_id}))

    else:
        form = BoardsForm()

    context = {
        'store':store,
        'form':form
    }
    return render(request,'mainpage/post_write.html', context)