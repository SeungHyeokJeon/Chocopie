import json
from pathlib import Path
import math
from collections import OrderedDict

from django.http  import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from accounts.models import Userinfo
from board.models import Stores, Boards, Items, Comments
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
            userInstance = Userinfo(id=User.objects.get(id=authId), provider=provider, name=name, date_joined=timezone.now())
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
    search_param = request.POST.get('search') # 검색 값이 존재하면 가져오기

    # 찜한가게와 일반 카테고리일때 데이터 불러오는 구문 변경
    if item=='찜한가게':
        authId = request.session.get('_auth_user_id')
        userinfo = Userinfo.objects.get(id=authId)
        likeStores = userinfo.like_store.split(',')
        likeStores = ' '.join(likeStores).split()

        if likeStores:
            query = Q()
            for idx in likeStores:
                query.add(Q(id=idx),query.OR)
            data = Stores.objects.filter(query).order_by('id')
        else:
            data=""

    else:
        marketNum = request.session['marketNum'] # 시장번호
        if search_param!=None and search_param!='None' and search_param!='': # 검색 값이 있을경우 해당하는 가게만 검색
            data = Stores.objects.filter(category=item, market_id=marketNum, name__contains=search_param).order_by('id')
        else:
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
        'item' : item,
        'search_param' : search_param
    }
    return render(request, 'mainpage/store.html', context)

def storepage_ajax(request):
    item = request.POST.get('item')
    search_param = request.POST.get('search_param') # 검색 값이 존재하면 가져오기
    # 페이지를 이동하면 무조건 최신순으로 정렬되고, radio 버튼 클릭시에만 동적으로 화면 변화시키기 위해 _ajax에만 작성
    order = request.POST.get('order') if request.POST.get('order')!='None' else 'id' # 특정 기준 정렬

    # 찜한가게와 일반 카테고리일때 데이터 불러오는 구문 변경
    if item=='찜한가게':
        authId = request.session.get('_auth_user_id')
        userinfo = Userinfo.objects.get(id=authId)
        likeStores = userinfo.like_store.split(',')
        likeStores = ' '.join(likeStores).split()

        if likeStores:
            query = Q()
            for idx in likeStores:
                query.add(Q(id=idx),query.OR)
            data = Stores.objects.filter(query).order_by(order)
        else:
            data=""

    else:
        marketNum = request.session['marketNum'] # 시장번호

        if search_param!='None' and search_param!='': # 검색 값이 있을경우 해당하는 가게만 검색
            data = Stores.objects.filter(category=item, market_id=marketNum, name__contains=search_param).order_by(order)
        else:
            data = Stores.objects.filter(category=item, market_id=marketNum).order_by(order)

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
        'item' : item,
        'search_param' : search_param,
        'order' : order
    }
    return render(request, 'mainpage/store_list_ajax.html', context)

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

def saveStore(request):
    if(request.method == 'POST'):
        stores = Stores()
        print(request.POST['owner'])
        stores.owner = Userinfo.objects.get(id=int(request.POST['owner']))
        stores.market = traditional_market.objects.get(id=int(request.POST['marketNum']))

        stores.name = request.POST['name']
        stores.category = request.POST['category']
        stores.address = request.POST['address'] + ',' + request.POST['addressSub']
        stores.introduce = request.POST['introduce']
        #post.user = request.user
        stores.mainimage = request.FILES['imgs']
            
        stores.date_joined = timezone.now()
        # 데이터베이스에 저장
        stores.save()
        return redirect(reverse('mainpage:detailStore', kwargs={'store_id':stores.id}))
    else:
        return redirect(reverse('mainpage:mainpage'))
    
def map(request):
    traditional_markets = traditional_market.objects.filter(

    ).values('id', 'name', 'road_address', 'latitude', 'longitude')
    context = {'traditional_markets':traditional_markets}
    return render(request, 'mainpage/map.html', context)

def heartStore(request):
    if(request.method == 'POST'):
        authId = request.session.get('_auth_user_id')
        store_id = request.POST['store_id']
        User = Userinfo.objects.get(id=authId)
        
        if User.like_store is not None:
            likeList = User.like_store.split(',')
        
            if store_id not in likeList:
                User.like_store = User.like_store + store_id +','
            else:
                likeList.remove(store_id)
                User.like_store = ",".join(likeList)
        else:
            User.like_store = store_id +','

        User.save()
    return JsonResponse({'message': 'SUCCESS'}, status=200)

def detailStore(request, store_id):
    search_param = request.POST.get('search') # 검색 값이 존재하면 가져오기

    store = Stores.objects.get(id=int(store_id))
    owner = Userinfo.objects.get(id=int(store.owner_id))

    if search_param!=None and search_param!='None' and search_param!='':
        board = Boards.objects.filter(store=int(store_id), title__contains=search_param).order_by('-id')
    else:
        board = Boards.objects.filter(store=int(store_id)).order_by('-id')

    # item, comment 불러오기
    query = Q()
    for idx in board:
        query.add(Q(board_id=idx.id),query.OR)
    items = Items.objects.filter(query)
    comments = Comments.objects.filter(query)

    listLength = 5  # 한번에 불러올 게시글 개수
    totalPage = math.ceil(len(board)/listLength) # 전체 페이지 계산

    paginator = Paginator(board,listLength) # 게시글 나누기
    page = request.POST.get('page') # page 파라미터 있으면 갖고오기
    
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
        'item' : items,
        'comment': comments,
        'totalPage':totalPage,
        'search_param' : search_param,
    }
    return render(request, 'mainpage/store_info.html', data)

def detailStore_ajax(request, id):
    search_param = request.POST.get('search_param') # 검색 값이 존재하면 가져오기
    # 페이지를 이동하면 무조건 최신순으로 정렬되고, radio 버튼 클릭시에만 동적으로 화면 변화시키기 위해 _ajax에만 작성
    order = request.POST.get('order') if request.POST.get('order')!='None' else 'id' # 특정 기준 정렬

    if search_param!='None' and search_param!='':
        board = Boards.objects.filter(store=id, title__contains=search_param).order_by('-'+order)
    else:
        board = Boards.objects.filter(store=id).order_by('-'+order)

    # item 불러오기
    query = Q()
    for idx in board:
        query.add(Q(board_id=idx.id),query.OR)
    items = Items.objects.filter(query)

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
        'totalPage':totalPage,
        'item' : items,
        'search_param' : search_param,
        'order': order
    }
    return render(request, 'mainpage/board_ajax.html', context)

def cart(request):
    authId = request.session.get('_auth_user_id')

    user = Userinfo.objects.get(id=authId)
    jsonData = user.shopping_basket

    if request.method == "POST":
        store_id = request.POST['storeid']
        id_list = request.POST.getlist('id_list[]')
        count_list = request.POST.getlist('count_list[]')

        # 장바구니에 등록된 상품이 있는지 확인하기
        if store_id in jsonData:
            # 장바구니에 있으면 해당 상점의 장바구니에 항목 추가하기
            for i in jsonData:
                if i==store_id:
                    if len(id_list)>1:
                        for id, count in zip(id_list, count_list):
                            print(id,count)
                            jsonData[i].append({'itemid':id,'count':count})
                    else:
                        jsonData[i].append({'itemid':id_list[0],'count':count_list[0]})

        else:
            # 장바구니에 없으면 새로 만들어서 추가하기
            jsonData[store_id]=[]
            if len(id_list)>1:
                for id, count in zip(id_list, count_list):
                    jsonData[store_id].append({'itemid':id,'count':count})
            else:
                jsonData[store_id].append({'itemid':id_list[0],'count':count_list[0]})

        # 항목 업데이트
        user.shopping_basket = jsonData
        user.save()
                
    # 장바구니에 들어있을경우
    if jsonData:
        # 상점 정보 불러오기
        query = Q()
        for idx in jsonData:
            query.add(Q(id=idx),query.OR)
        store = Stores.objects.filter(query).order_by('id')
    
        # 상품 불러오기 및 상품 수량 저장하기
        query = Q()
        itemcount = {}
        for storeid in jsonData:
            for idx in jsonData[storeid]:
                query.add(Q(id=idx['itemid']),query.OR)
                itemcount[idx['itemid']]=idx['count']
        item = Items.objects.filter(query).order_by('id')

        # 가게별 물건 총합 계산
        price = {}
        # 총합 초기화
        for idx in store:
            price[idx.id]=0

        # 총합 계산
        for item_idx in item:
            for itemcount_idx in itemcount:
                if itemcount_idx==str(item_idx.id):
                    for store_idx in store:
                        if item_idx.store_id.id==store_idx.id:
                            # 모든 조건이 만족하면 해당 가게 총합 추가
                            prices = int(itemcount[itemcount_idx])*item_idx.price
                            price[store_idx.id]+=prices

        # 장바구니 들어 있는 모든 물품 총합 계산
        total=0
        for idx in price:
            total+=price[idx]
        price['total'] = total

        context = {
            'users':user,
            'store':store,
            'item':item,
            'itemcounts':itemcount,
            'totalprice':price,
        }

    # 장바구니에 등록된 상품이 없을경우
    else:
        context = {
            'users':user,
        }
    return render(request, 'mainpage/cart.html', context)

def mypage(request):
    authId = request.session.get('_auth_user_id')
    userinfo = Userinfo.objects.get(id=authId)
    data = {
        'userinfo':userinfo,
    }
    return render(request, 'mainpage/mypage.html', data)

def userConfig(request, element_id):
    userid = request.POST['owner']
    if element_id == "name":
        User = Userinfo.objects.get(id=userid)
        User.name = request.POST['name']
        User.save()

    elif element_id == "gender":
        User = Userinfo.objects.get(id=userid)
        User.gender = False if request.POST['gender'] == "남성" else True
        User.save()

    elif element_id == "birthday":
        User = Userinfo.objects.get(id=userid)
        User.birthday = request.POST['birthday']
        User.save()

    elif element_id == "address":
        User = Userinfo.objects.get(id=userid)
        User.address = request.POST['address'] + "," + request.POST['addressSub']
        User.save()

    else:
        return JsonResponse({'message': 'ERROR'}, status=401)
    return JsonResponse({'message': 'SUCCESS'}, status=200)


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
            # 게시글 먼저 등록
            post = Boards()
            post.store=store
            post.writer=userinfo
            post.writer_name=userinfo.name
            post.title = request.POST.get('title')
            post.content = request.POST.get('content')
            post.thumbnail = request.POST.get('thumbnail')
            post.views=0
            post.date_posted=timezone.now()

            post.save()
            

            # 등록된 게시글 통해 item 등록
            uploadedPost = Boards.objects.get(writer=post.writer, date_posted=post.date_posted)

            itemname = request.POST.getlist('itemname[]')
            itemprice = request.POST.getlist('itemprice[]')
            # itemcount = request.POST.getlist('itemcount[]')
            
            for name, price in zip(itemname, itemprice):
                item = Items()
                item.name=name
                item.price=price
                item.board_id=uploadedPost
                item.store_id=store
                item.save()

            # 등록된 게시글에 item항목 추가
            itemList = Items.objects.filter(board_id=uploadedPost)

            itemId = ''
            for idx in itemList: # item 번호 이어 붙이기
                itemId += str(idx.id)+','

            uploadedPost.item = itemId
            uploadedPost.save()

            return redirect(reverse('mainpage:detailStore', kwargs={'store_id':store_id}))

    else:
        form = BoardsForm()

    context = {
        'store':store,
        'form':form
    }
    return render(request,'mainpage/post_write.html', context)

def addComment(request, board_id):
    authId = request.session.get('_auth_user_id')
    userinfo = Userinfo.objects.get(id=authId)
    board = Boards.objects.get(id=board_id)

    context={}
    if request.method == "POST":
        if request.POST['add'] == 'true':
            comment = Comments()

            comment.board = board
            comment.writer = userinfo
            comment.writer_name = userinfo.name
            comment.content = request.POST['comment']
            nowDate = timezone.now()
            comment.date_posted = nowDate

            comment.save()
            
            commentData = Comments.objects.get(writer = userinfo, date_posted=nowDate)

            context = {
                'comment': commentData,
                'board': board,
            }

        elif request.POST['add'] == 'first':
            commentData = Comments.objects.filter(board=board_id).order_by('id')

            if commentData.count()-2<0:
                length=0
            else:
                length=commentData.count()-2

            commentData = commentData[length:]
            context = {
                'comment': commentData,
                'board': board,
            }

        else:
            commentData = Comments.objects.filter(board=board_id).order_by('id')

            if commentData.count()-2<0:
                length=commentData.count()
            else:
                length=commentData.count()-2

            commentData = commentData[:length]

            context = {
                'comment': commentData,
                'board': board,
            }

    
    return render(request, 'mainpage/comment_ajax.html', context)