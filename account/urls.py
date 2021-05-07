from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('loginKakao/', views.loginKakao, name='loginKakao'),
    path('loginRedirectKakao/', views.loginRedirectKakao, name='loginRedirectKakao'),
    path('logoutKakao/', views.logoutKakao, name='logoutKakao'),
]