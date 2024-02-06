from rest_framework import serializers
from .models import RequestStore

class RequestStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestStore
        fields = '__all__'