from django.db import models
from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken

# Create your models here.
class Userinfo(models.Model):
    id = models.OneToOneField(User, models.CASCADE, db_column='id', primary_key=True)
    provider = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(db_column='NAME', max_length=64, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(max_length=64, blank=True, null=True)
    date_joined = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'userinfo'