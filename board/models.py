from django.db import models

# Create your models here.
class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'

class SocialaccountSocialaccount(models.Model):
    id = models.BigAutoField(primary_key=True)
    provider = models.CharField(max_length=30)
    uid = models.CharField(max_length=191)
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    extra_data = models.TextField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialaccount'
        unique_together = (('provider', 'uid'),)

class SocialaccountSocialapp(models.Model):
    id = models.BigAutoField(primary_key=True)
    provider = models.CharField(max_length=30)
    name = models.CharField(max_length=40)
    client_id = models.CharField(max_length=191)
    secret = models.CharField(max_length=191)
    key = models.CharField(max_length=191)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialapp'

class SocialaccountSocialtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.TextField()
    token_secret = models.TextField()
    expires_at = models.DateTimeField(blank=True, null=True)
    account = models.ForeignKey(SocialaccountSocialaccount, models.DO_NOTHING)
    app = models.ForeignKey(SocialaccountSocialapp, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialtoken'
        unique_together = (('app', 'account'),)

class Users(models.Model):
    id = models.OneToOneField(SocialaccountSocialaccount, models.CASCADE, db_column='id', primary_key=True)
    provider = models.CharField(max_length=30, blank=True, null=True)
    userid = models.CharField(max_length=64, blank=True, null=True)
    password = models.CharField(db_column='PASSWORD', max_length=64, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=64, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(max_length=64, blank=True, null=True)
    date_joined = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'

class Stores(models.Model):
    id = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey('Users', models.CASCADE)
    category = models.CharField(max_length=11, blank=True, null=True)
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    mainimage = models.CharField(max_length=64, blank=True, null=True)
    sales = models.TextField(blank=True, null=True)
    date_joined = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stores'

class Boards(models.Model):
    id = models.BigAutoField(primary_key=True)
    store = models.ForeignKey('Stores', models.CASCADE)
    writer = models.ForeignKey('Users', models.DO_NOTHING)
    writer_name = models.CharField(max_length=10)
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)
    is_noticed = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'boards'

class Comments(models.Model):
    id = models.BigAutoField(primary_key=True)
    board = models.ForeignKey('Boards', models.CASCADE)
    writer = models.ForeignKey('Users', models.DO_NOTHING)
    writer_name = models.CharField(max_length=10)
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)
    is_noticed = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'comments'
