from django.db import models

# Create your models here.
class traditional_market(models.Model):
    name = models.TextField()
    market_type = models.TextField()
    road_address = models.TextField()
    number_address = models.TextField()
    latitude = models.DecimalField(max_digits = 7, decimal_places = 5) #위도
    longitude = models.DecimalField(max_digits = 7, decimal_places = 4) #경도
    handling_item =  models.TextField() #취급품목
    opening_year = models.TextField()
    phone_number = models.TextField()

    class Meta:
        managed = False
        db_table = 'traditional_market'