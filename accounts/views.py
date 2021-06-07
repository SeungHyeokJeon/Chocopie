from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http  import JsonResponse, HttpResponse
from django.contrib import messages

from accounts.models import Userinfo, PhoneVerification
from django.contrib.auth.models import User # auth_user
from allauth.socialaccount.models import SocialAccount, SocialToken
from allauth.account.models import EmailAddress
from django.contrib.sessions.models import Session

from random import randint
import base64
import requests
import json
import time
import hmac
import hashlib


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

def SMSVerificationView(request):
    if request.method == 'POST': 
        phone = request.POST['phone'] 
    code = str(randint(100000, 999999))
    #update_or_creaete(조건, defaults = 생성할 데이터 값)
    PhoneVerification.objects.update_or_create(
        phone=phone,
        defaults={
            'phone': phone,
            'code' : code
        }
    )
                
    # phone, code 를 인자로 send_verification 메서드를 호출
    send_verification(
        phone=phone,
        code=code
    )
    messages.info(request, 'Your password has been changed successfully!')
    return JsonResponse({'message': 'SUCCESS'}, status=201)

#SMS 보내기 https://g-y-e-o-m.tistory.com/167
def send_verification(phone, code):
    SMS_URL = 'https://sens.apigw.ntruss.com/sms/v2/services/' + 'ncp:sms:kr:268092361152:chocopie' + '/messages'
    timestamp = str(int(time.time() * 1000))
    secret_key = bytes('WkJaTeXLfBRxK1YqTC0BTOHxDDwi3jnrqK1O1Z2i', 'utf-8')
    
    method = 'POST'
    uri = '/sms/v2/services/' + 'ncp:sms:kr:268092361152:chocopie' + '/messages'
    message = method + ' ' + uri + '\n' + timestamp + '\n' + '89RI6QSTxvJaZWR5s35W'
    message = bytes(message, 'utf-8')

            
    # 알고리즘으로 암호화 후, base64로 인코딩
    signingKey = base64.b64encode(
        hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())

    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': '89RI6QSTxvJaZWR5s35W',
        'x-ncp-apigw-signature-v2': signingKey,
    }

    body = {
        'type': 'SMS',
        'contentType': 'COMM',
        'countryCode': '82',
        'from': "01041840152",
        'content': f'인녕하세요. 정통시장입니다. 인증번호 [{code}]를 입력해주세요.',
        'messages': [
            {
                'to': phone,
            }
        ]
    }

    # body를 json으로 변환
    encoded_data = json.dumps(body)
    
    # post 메서드로 데이터를 보냄
    res = requests.post(SMS_URL, headers=headers, data=encoded_data)
    return HttpResponse(res.status_code)

# 문자인증 확인과정
def SMSConfirmView(request):
    if request.method == 'POST': 
        phone = request.POST['phone'] 
        verification_number = request.POST['code']
        userid = request.POST['owner']
        
        if verification_number == PhoneVerification.objects.get(phone=phone).code:
            User = Userinfo.objects.get(id=userid)
            User.phone = phone
            User.save()
            return JsonResponse({'message': 'SUCCESS'}, status=200)
        else:
            return JsonResponse({'message': 'REGISTERED_NUMBER'}, status=401)
        return JsonResponse({'message': 'INVALID_NUMBER'}, status=401)