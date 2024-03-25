from rest_framework import serializers
from api.Models.ParkingLotDetails import ParkingLotDetails

class ParkingLotDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingLotDetails
        fields = ['id','name']