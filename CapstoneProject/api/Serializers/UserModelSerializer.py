from rest_framework import serializers
from api.Models.UserModel import UserModel

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email','full_name','phone']