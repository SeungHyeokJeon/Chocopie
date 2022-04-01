# Capstone Project
## 소개
![marketmain](https://user-images.githubusercontent.com/15073430/161207579-f890d1ce-4efb-468a-8991-dcac0a82c29f.png)  
상인이 직접 작성한 가게 상품 소개 글을 통해 가게 및 상품을 홍보하고 댓글을 통해 고객과 소통할 수 있는 서비스
## 주요 기능
![function](https://user-images.githubusercontent.com/15073430/161207831-a457ad59-1bac-4205-aa7d-1ec84a264ef4.png)
### 로그인
![noname01](https://user-images.githubusercontent.com/15073430/161208084-82d58971-b352-4d82-8a65-159666686c02.png)
### 회원정보 수정
![noname09](https://user-images.githubusercontent.com/15073430/161208371-605d9654-0c48-446b-8f44-2b293b93d6f8.png)
### 시장 찾기
![noname02](https://user-images.githubusercontent.com/15073430/161208203-bb3035f7-ca1c-4a68-badc-2c1ccebb3ae8.png)
### 장바구니
![noname06](https://user-images.githubusercontent.com/15073430/161208280-6a40e718-6939-4eae-9f37-3f0bc4cb2665.png)
### 결제
![noname08](https://user-images.githubusercontent.com/15073430/161208310-5a928d73-6956-40ce-9d1c-5a071465cb13.png)
### 가게생성
![noname111](https://user-images.githubusercontent.com/15073430/161208583-295188f0-c97d-4bd5-bc21-90841cd3df8c.png)
### 주문관리
![333](https://user-images.githubusercontent.com/15073430/161208578-3f9ea4dc-a8c4-49cf-ade4-0f6e6ea3587d.png)

## Requirement

- django!

- mysqlclient
### Installation and Run Sever


```bash
$ pip install django==3.2
$ pip install mysqlclient![Uploading noname06.png…]()

$ pip install django-allauth
$ pip install pillow
$ pip install django-summernote
```
- 실행 전 Notion/Django/Secrets에 있는 Secrets.json파일을 받아 최상위 폴더에 저장
```bash
../Chocopie/ $ python manage.py makemigrations
../Chocopie/ $ python manage.py migrate
```

```bash
# run server
../Chocopie/ $ python manage.py runserver
```
## **Stack**

`Python` `Django` `MariaDB`

### 필독사항

- settings.py에 들어간 비밀키와 db정보는 Notion/Django/Secrets 항목 확인할 것
