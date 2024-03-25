from rest_framework import serializers
from api.Models.BookingSession import BookingSession

class BookingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingSession
        fields = ['session_id','booking_time','calculated_bill','parking_out_time']