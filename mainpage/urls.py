from django.urls import path
from . import views

app_name = 'mainpage'
urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('map/', views.map, name='map'),
    path('storepage/<str:item>', views.storepage, name='storepage'),
    path('storepage/ajax/',views.storepage_ajax, name="storepage_ajax"),
    path('detail/<int:store_id>',views.detailStore, name='detailStore'),
    path('detail/<str:id>/ajax',views.detailStore_ajax, name='detailStore_ajax'),
    path('detail/<str:store_id>/postwrite', views.post_write, name='post_write'),
    path('makestore/',views.makestore, name='makestore'),
    path('savestore/',views.saveStore, name='saveStore'),
    path('mypage/',views.mypage, name='mypage'),
    #path('store/',views.store, name='store'),
    #path('dbupload/', views.dbupload, name='dbupload'),
]