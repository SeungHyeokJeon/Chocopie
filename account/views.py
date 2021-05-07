from django.shortcuts import render, redirect
import requests
import json

# Create your views here.
def login(request):
    return render(request, 'account/login.html')

def logout(request):
    return render(request, 'account/logout.html')

def loginKakao(request):
    restApiKey = 'cc4da3338c1087e45c43b48a355072be'
    redirectUrl = 'http://127.0.0.1:8000/account/loginRedirectKakao'
    url = f'https://kauth.kakao.com/oauth/authorize?client_id={restApiKey}&redirect_uri={redirectUrl}&response_type=code'
    return redirect(url)

def loginRedirectKakao(request):
    qs = request.GET['code']
    restApiKey = 'cc4da3338c1087e45c43b48a355072be'
    redirectUrl = 'http://127.0.0.1:8000/account/loginRedirectKakao'
    url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={restApiKey}&redirect_uri={redirectUrl}&code={qs}'
    res = requests.post(url)
    result=res.json()
    request.session['access_token'] = result['access_token']
    request.session.modified = True
    return redirect('/index/')

def logoutKakao(request):
    token = request.session['access_token']
    url = 'https://kapi.kakao.com/v1/user/logout'
    #url = 'https://kapi.kakao.com/v1/user/unlink'  #회원탈퇴
    header = {
        'Authorization': f'bearer {token}'
    }

    res = requests.post(url, headers=header)
    result = res.json()
    if result.get('id'):
        del request.session['access_token']
        return redirect('/index/')
    else:
        #return render(request, 'index/index.html', {"fail":True})
        return redirect('/index/')