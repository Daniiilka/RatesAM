from django.db import models
from django.utils import timezone
from datetime import datetime

now = datetime.now()
current_time = now.strftime("%d-%m-%Y %H-%M")


# Create your models here.


class Currency(models.Model):
    rub_usd_uni = models.FloatField(default=None)
    rub_eur_uni = models.FloatField(default=None)
    rub_amd_uni = models.FloatField(default=None)
    usd_amd_sas = models.FloatField(default=None)
    eur_amd_sas = models.FloatField(default=None)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.last_update
