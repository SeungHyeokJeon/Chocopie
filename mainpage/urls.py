from django.urls import path
from . import views

app_name = 'mainpage'
urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('store/', views.storepage, name='storepage'),
]