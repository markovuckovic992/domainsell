from django.db import models
from django.utils import timezone

class Offer(models.Model):
    lead = models.CharField(max_length=100)
    drop = models.CharField(max_length=100)
    amount = models.FloatField(blank=True, null=True)
    offer_id = models.CharField(max_length=10)
    base_id = models.IntegerField()
    hash_base_id = models.CharField(max_length=32, unique=True)
    email = models.CharField(max_length=320, blank=True, null=True)
    remail = models.CharField(max_length=320, blank=True, null=True)
    contact = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(max_length=5, blank=True, null=True)
    sale = models.SmallIntegerField(default=0)

    date_started = models.DateField(default=timezone.now)
    date = models.DateField(blank=True, null=True)
    updated = models.DateField(blank=True, null=True)
    status = models.SmallIntegerField(default=0)

    stage = models.SmallIntegerField(default=1)
    phase = models.SmallIntegerField(default=0)
    last_email_date = models.DateTimeField(default=timezone.now)
    done = models.SmallIntegerField(default=0)

    class Meta:
        db_table = 'offers'


class BlackList(models.Model):
    email = models.CharField(max_length=320, blank=True, null=True)

    class Meta:
        db_table = 'blacklist'


class Setting(models.Model):
    last_id = models.IntegerField(default=0)

    class Meta:
        db_table = 'Setting'

class controlPanel(models.Model):
    tip = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    distance = models.IntegerField(default=0)

    class Meta:
        db_table = 'controlPanel'
