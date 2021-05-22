from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('loginKakao/', views.loginKakao, name='loginKakao'),
    path('register/',views.register, name='register'),
]