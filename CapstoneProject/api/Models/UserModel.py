from django.db import models

class UserModel(models.Model):
    user_id = models.BigAutoField(primary_key= True)
    email = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    intent = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone = models.BigIntegerField(blank=False)
    processed = models.CharField(max_length=5,default='False')

    class Meta:
        db_table = "users"