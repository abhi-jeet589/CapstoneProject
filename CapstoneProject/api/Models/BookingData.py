from django.db import models


class BookingData(models.Model):
    booking_id = models.BigAutoField(primary_key=True,blank=False)
    place_id = models.CharField(max_length=255,blank=False)
    vip = models.CharField(max_length=255,blank=False)
    car_number_plate = models.CharField(max_length=255,blank=False)
    user_id = models.BigIntegerField(blank=False)
    booking = models.DateTimeField(blank=False)

    class Meta:
        db_table = "bookings"