from django.db import models
from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
import requests
from random import randint

# Create your models here.
class PhoneVerification(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    phone = models.CharField(unique=True, max_length=11)
    code  = models.CharField(max_length=6)
    
    class Meta:
        db_table = 'phone_verifications'

class Userinfo(models.Model):
    id = models.OneToOneField(User, models.CASCADE, db_column='id', primary_key=True)
    provider = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(db_column='NAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    gender = models.BooleanField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=256, blank=True, null=True)
    address = models.CharField(max_length=1024, blank=True, null=True)
    date_joined = models.DateTimeField(blank=True, null=True)
    like_store = models.CharField(max_length=30, blank=True, null=True)
    shopping_basket = models.JSONField(default={}, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'userinfo'

class OrderList(models.Model):
    id = models.BigAutoField(primary_key=True)
    store = models.ForeignKey('board.Stores', models.DO_NOTHING)
    user = models.ForeignKey(Userinfo, models.CASCADE)
    user_name = models.CharField(db_column='NAME', max_length=256, blank=True, null=True)
    user_email = models.CharField(max_length=256, blank=True, null=True)
    board = models.ForeignKey('board.Boards', models.DO_NOTHING)
    item = models.ForeignKey('board.Items', models.DO_NOTHING)
    item_name = models.CharField(max_length=256)
    item_ea = models.IntegerField(blank=True, null=True)
    item_price = models.IntegerField(blank=True, null=True)
    shipping_address = models.CharField(max_length=1024, blank=True, null=True)
    order_date = models.DateTimeField(blank=True, null=True)
    shipping_date = models.DateTimeField(blank=True, null=True)
    order_status = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed=True
        db_table = 'orderlist'