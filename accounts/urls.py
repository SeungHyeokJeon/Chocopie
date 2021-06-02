from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('withdrawal/', views.withdrawal, name='withdrawal'),
    path('loginKakao/', views.loginKakao, name='loginKakao'),
    path('register/',views.register, name='register'),
    path('withdrawal/process/', views.withdrawalProcess, name='withdrawalProcess'),
]