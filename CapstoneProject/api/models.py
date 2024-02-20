from django.db import models

class RequestStore(models.Model):
    request = models.CharField(max_length=200,blank=False)
    response = models.JSONField()
    req_received_at = models.DateTimeField(auto_now = True,auto_created=True)
    res_received_at = models.DateTimeField(auto_now = True,auto_created=True)

    def __str__(self) -> str:
        return self.request + ' ' + self.response