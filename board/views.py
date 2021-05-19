import math

from django.shortcuts import render
from board.models import Stores
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def test(request):
    data = Stores.objects.all() # db 전체 값 가져오기
    
    listLength = 5  # 한번에 불러올 게시글 개수
    totalPage = math.ceil(len(data)/listLength) # 전체 페이지 계산

    paginator = Paginator(data,listLength) # 게시글 나누기
    page = request.GET.get('page') # page 파라미터 있으면 갖고오기
    
    try:
        post_list=paginator.page(page) # 현재 페이지 지정
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)

    context = {'post_list':post_list, 'totalPage':totalPage}
    return render(request,'board/test.html', context)

# 추가될 요소 접근
def test_ajax(request):
    data = Stores.objects.all()

    listLength = 5
    totalPage = math.ceil(len(data)/listLength)

    paginator = Paginator(data,listLength)
    page = request.POST.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    context = {'post_list':post_list, 'totalPage':totalPage}
    return render(request, 'board/test_ajax.html', context)