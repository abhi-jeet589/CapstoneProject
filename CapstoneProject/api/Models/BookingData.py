from django.db import models


class BookingData(models.Model):
    booking_id = models.BigAutoField(primary_key=True)
    booking_date_time = models.DateTimeField()
    booking_type = models.CharField(max_length=255)
    car_number_plate = models.CharField(max_length=255)
    parking_in_time = models.DateTimeField()
    place_id = models.BigIntegerField()
    total_hours_stayed = models.BigIntegerField()
    user_id = models.CharField(max_length=255)

    class Meta:
        db_table = "parking_bookings"