from django.db import models

class ParkingLotDetails(models.Model):
    id = models.BigAutoField(primary_key= True)
    name = models.CharField(max_length=255,blank=False)
    address = models.CharField(max_length=255,blank=False)
    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)
    capacity = models.IntegerField(blank=False)
    available_parking_spot = models.IntegerField(blank=False)
    open_space = models.SmallIntegerField(blank=False)
    covered = models.SmallIntegerField(blank=False)
    CCTV = models.SmallIntegerField(blank=False)
    gated = models.SmallIntegerField(blank=False)
    accessible_spot = models.SmallIntegerField(blank=False)
    open_space_availability = models.IntegerField(blank=False)
    covered_availability = models.IntegerField(blank=False)
    accessible_spot_availability = models.IntegerField(blank=False)
    min_park_time = models.CharField(max_length=10,blank=False)
    operation_hour = models.CharField(max_length=10,blank=False)

    class Meta:
        db_table = "parking_lot_details"