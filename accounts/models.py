from django.db import models
from django.conf import settings
#Create your models here.
# class User(models.Model):
#     account_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
#     provider = models.CharField(max_length=30, blank=True, null=True)
#     userid = models.CharField(max_length=64, blank=True, null=True)
#     password = models.CharField(db_column='PASSWORD', max_length=64, blank=True, null=True)  # Field name made lowercase.
#     name = models.CharField(db_column='NAME', max_length=64, blank=True, null=True)  # Field name made lowercase.
#     email = models.CharField(max_length=64, blank=True, null=True)
#     date_joined = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'user'
