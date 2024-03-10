from django.db import models

class RequestStore(models.Model):
    request = models.CharField(max_length=200,blank=False)
    response = models.JSONField()
    req_received_at = models.DateTimeField(auto_now = True,auto_created=True)
    res_received_at = models.DateTimeField(auto_now = True,auto_created=True)

    def __str__(self) -> str:
        return self.request + ' ' + self.response
    
    class Meta:
        db_table = "req"


class UserAnalyticsData(models.Model):
    date_processed = models.DateField(blank = False)
    no_of_users = models.BigIntegerField(blank = False)

    class Meta:
        db_table = "user_analytics"


class BookingData(models.Model):
    booking_id = models.BigAutoField(primary_key=True,blank=False)
    place_id = models.CharField(max_length=255,blank=False)
    vip = models.CharField(max_length=255,blank=False)
    car_number_plate = models.CharField(max_length=255,blank=False)
    user_id = models.BigIntegerField(blank=False)
    booking = models.DateTimeField(blank=False)

    class Meta:
        db_table = "bookings"