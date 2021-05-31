# accounts/models.py
from django.db import models
from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from accounts.models import Userinfo

# Create your models here.
# Stores Models은 임시로 여기다 배치함
class Stores(models.Model):
    owner = models.ForeignKey(Userinfo, models.CASCADE)
    category = models.CharField(max_length=11, blank=True, null=True)
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=1024, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    mainimage = models.CharField(max_length=64, blank=True, null=True)
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
    views = models.IntegerField(blank=True, null=True)
    date_posted = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)
    is_noticed = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'boards'

class Comments(models.Model):
    id = models.BigAutoField(primary_key=True)
    board = models.ForeignKey(Boards, models.CASCADE)
    writer = models.ForeignKey(Userinfo, models.DO_NOTHING)
    writer_name = models.CharField(max_length=256)
    content = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'comments'