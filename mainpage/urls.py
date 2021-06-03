from django.urls import path
from . import views

app_name = 'mainpage'
urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('map/', views.map, name='map'),
    path('storepage/<str:item>', views.storepage, name='storepage'),
    path('storepage/ajax/',views.storepage_ajax, name="storepage_ajax"),
    path('storeinfo/<str:id>',views.storeInfo, name='storeInfo'),
    path('storeinfo/<str:id>/ajax',views.storeInfo_ajax, name='storeInfo_ajax'),
    path('store/',views.store, name='store'),
    path('makestore/',views.makestore, name='makestore'),
    path('mypage/',views.mypage, name='mypage'),
    path('dbupload/', views.dbupload, name='dbupload'),
]