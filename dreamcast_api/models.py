from django.db import models
from django.utils import timezone


class Wants(models.Model):
    """
    
    """
    id = models.AutoField(primary_key=True)
    want = models.CharField(max_length=1000, null=True, blank=True)
    manifested_on = models.DateTimeField(null=True, blank=True, default=timezone.now)

    class Meta:
        db_table = "wants"
