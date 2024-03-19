from rest_framework import serializers
from api.Models.RevenueAnalyticsData import RevenueAnalyticsData


class RevenueAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevenueAnalyticsData
        fields = ['date_processed','revenue']