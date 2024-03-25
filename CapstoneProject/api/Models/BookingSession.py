from django.db import models

class BookingSession(models.Model):
    session_id = models.BigAutoField(primary_key= True)
    booking_id = models.BigIntegerField()
    booking_time = models.DateTimeField()
    calculated_bill = models.FloatField()
    parking_out_time = models.DateTimeField()
    processed = models.CharField(max_length=5,default='False')

    class Meta:
        db_table = "booking_sessions"