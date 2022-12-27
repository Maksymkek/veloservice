from datetime import datetime
from xmlrpc.client import DateTime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class BicycleStation(models.Model):
    name = models.CharField('Station name', max_length=50)

    def get_absolute_url(self):
        return f'/{self.id}'


class Bicycle(models.Model):
    station = models.ForeignKey(BicycleStation, on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name='Bicycle photo', upload_to='bicycles/', blank=True, null=True)
    name = models.CharField('Bicycle name', max_length=50)
    description = models.TextField('Description')
    usages = models.PositiveIntegerField('Amount of usages')
    status = models.CharField('Status', max_length=50,default="free")
    price = models.PositiveIntegerField('Hire price')
    user = models.PositiveIntegerField("Sharing user", default=0)

    def get_absolute_url(self):
        return f'/{self.id}'


class Order(models.Model):
    user_id = models.PositiveIntegerField("User id")
    bike = models.ForeignKey(Bicycle, verbose_name="Bike", on_delete=models.CASCADE)
    usageTime = models.PositiveIntegerField("Rental time")
    price = models.PositiveIntegerField("Rental price", default=0)
    returnTime = models.DateTimeField("Return time",default=datetime(2001,1,1,0,0))

    def get_absolute_url(self):
        return f'/{self.id}'

    def __str__(self):
        return ''.format(self.returnTime.strftime('%d.%m.%Y %H:%M'))
