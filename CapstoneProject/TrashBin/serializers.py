from rest_framework import serializers
from .models import RequestStore,UserAnalyticsData,BookingData

class RequestStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestStore
        fields = '__all__'


class UserAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnalyticsData
        fields = ['date_processed','no_of_users']


class BookingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingData
        fields = '__all__'