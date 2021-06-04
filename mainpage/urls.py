from django.urls import path
from . import views

app_name = 'mainpage'
urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('map/', views.map, name='map'),
    path('storepage/<str:item>', views.storepage, name='storepage'),
    path('storeinfo/',views.storeInfo, name='storeInfo'),
    #path('store/',views.store, name='store'),
    path('storepage/ajax/',views.storepage_ajax, name="storepage_ajax"),
    path('makestore/',views.makestore, name='makestore'),
    path('mypage/',views.mypage, name='mypage'),
    #path('dbupload/', views.dbupload, name='dbupload'),
    path('detail/<int:store_id>',views.detailStore, name='detailStore'),
    path('detail/<str:id>/ajax',views.detailStore_ajax, name='detailStore_ajax'),
]