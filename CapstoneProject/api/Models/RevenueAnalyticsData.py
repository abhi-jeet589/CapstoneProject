from django.db import models

class RevenueAnalyticsData(models.Model):
    date_processed = models.DateField(blank = False)
    revenue = models.BigIntegerField(blank = False)

    class Meta:
        db_table = "revenue_analytics"