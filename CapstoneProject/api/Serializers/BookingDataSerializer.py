from rest_framework import serializers
from api.Models.BookingData import BookingData

class BookingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingData
        fields = '__all__'