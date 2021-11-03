from django.urls import path
from . import views
from accounts.views import SMSVerificationView, SMSConfirmView

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
    path('configstore/<int:store_id>', views.configStore, name='configStore'),
    path('configstore2/<int:store_id>', views.configStore2, name='configStore2'),
    path('savestore/',views.saveStore, name='saveStore'),
    path('deletestore/<int:store_id>',views.deleteStore, name='deleteStore'),
    path('heartStore/', views.heartStore, name='heartStore'),
    path('cart/', views.cart, name='cart'),
    path('selectDelete/', views.selectDelete, name='selectDelete'),
    
    path('mypage/',views.mypage, name='mypage'),
    path('orderstatus/',views.orderstatus, name='orderstatus'),

    path('config/<str:element_id>',views.userConfig, name='userConfig'),
    path('sms/', SMSVerificationView, name='smsverification'),
    path('smsVerification/', SMSConfirmView, name='smsconfirm'),
    path('addComment/<int:board_id>', views.addComment, name='addComment'),
    #path('store/',views.store, name='store'),
    #path('dbupload/', views.dbupload, name='dbupload'),

    path('kakaoPay/', views.kakaoPay, name='kakaoPay'),
    path('kakaoPayLogic/', views.kakaoPayLogic, name='kakaoPayLogic')
]