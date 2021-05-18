from django.shortcuts import render, redirect
import requests
import json

# Create your views here.
def login(request):
    return render(request, 'accounts/login.html')

def logout(request):
    return render(request, 'accounts/logout.html')

def loginKakao(request):
    restApiKey = 'cc4da3338c1087e45c43b48a355072be'
    redirectUrl = 'http://127.0.0.1:8000/allauth/kakao/login/callback/'
    return redirect(f'https://kauth.kakao.com/oauth/authorize?client_id={restApiKey}&redirect_uri={redirectUrl}&response_type=code')