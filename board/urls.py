from django.urls import path
from . import views

app_name = 'board'
urlpatterns = [
    path('', views.test, name='test'),
    path('ajax/', views.test_ajax, name='test_ajax'),
]