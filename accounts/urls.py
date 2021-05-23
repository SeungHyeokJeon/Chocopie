from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('withdrawal/', views.withdrawal, name='withdrawal'),
    path('loginKakao/', views.loginKakao, name='loginKakao'),
    path('register/',views.register, name='register'),
    path('withdrawal/process/', views.withdrawalProcess, name='withdrawalProcess')
]