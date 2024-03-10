from rest_framework import serializers
from api.Models.UserAnalyticsData import UserAnalyticsData


class UserAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnalyticsData
        fields = ['date_processed','no_of_users']