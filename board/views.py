import math

from django.shortcuts import render
from board.models import Stores
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def test(request):
    #data = Stores.objects.all()
    data = list(range(1,30))

    listLength = 5
    totalPage = math.ceil(len(data)/listLength)

    paginator = Paginator(data,listLength)
    page = request.GET.get('page')
    
    try:
        post_list=paginator.page(page)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)

    context = {'post_list':post_list, 'totalPage':totalPage}
    return render(request,'board/test.html', context)

# 추가될 요소 접근
def test_ajax(request):
    #data = Stores.objects.all()
    data = list(range(1,30))

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