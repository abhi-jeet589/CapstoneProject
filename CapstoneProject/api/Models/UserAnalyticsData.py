from django.db import models

class UserAnalyticsData(models.Model):
    date_processed = models.DateField(blank = False)
    no_of_users = models.BigIntegerField(blank = False)

    class Meta:
        db_table = "user_analytics"