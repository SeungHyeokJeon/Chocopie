from django.db import models
from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken

# Create your models here.
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

    class Meta:
        managed = True
        db_table = 'userinfo'