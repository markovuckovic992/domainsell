from django.db import models


class Offer(models.Model):
    lead = models.CharField(max_length=100)
    amount = models.FloatField(blank=True, null=True)
    offer_id = models.CharField(max_length=10)
    base_id = models.IntegerField()
    hash_base_id = models.CharField(max_length=32, unique=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    contact = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'ponude'
