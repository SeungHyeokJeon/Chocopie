# accounts/models.py
from django.db import models
from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from accounts.models import Userinfo
from mainpage.models import traditional_market

# Create your models here.
# Stores Models은 임시로 여기다 배치함
class Stores(models.Model):
    owner = models.ForeignKey(Userinfo, models.CASCADE)
    market = models.ForeignKey(traditional_market, models.DO_NOTHING, null=True)
    category = models.CharField(max_length=11, blank=True, null=True)
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=1024, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    mainimage = models.ImageField(upload_to='images/',blank=True, null=True)
    introduce = models.CharField(max_length=256, blank=True, null=True)
    sales = models.TextField(blank=True, null=True)
    date_joined = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stores'

class Boards(models.Model):
    id = models.BigAutoField(primary_key=True)
    store = models.ForeignKey(Stores, models.CASCADE)
    writer = models.ForeignKey(Userinfo, models.DO_NOTHING)
    writer_name = models.CharField(max_length=256)
    title = models.CharField(max_length=1024)
    content = models.TextField(blank=True, null=True)
    item = models.TextField(blank=True, null=True) #json
    thumbnail = models.ImageField(upload_to='post_thumbnail/', blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    date_posted = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)
    is_noticed = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'boards'

class Comments(models.Model):
    id = models.BigAutoField(primary_key=True)
    board = models.ForeignKey(Boards, models.CASCADE)
    parent = models.ForeignKey('self', models.CASCADE, null=True)
    writer = models.ForeignKey(Userinfo, models.DO_NOTHING)
    writer_name = models.CharField(max_length=256)
    content = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'comments'