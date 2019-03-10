# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.

class Measurements(models.Model):
    room_Date = models.DateTimeField(default=datetime.now, blank=True)
    room_Temperature = models.FloatField()
    room_Humidity = models.FloatField(default=0)
    room_Pressure = models.FloatField(default=0)
    room_Light = models.FloatField(default=0)

    #Try To change DecimalField to FloatField to increase perfomance
    def __str__(self):
        return str(self.room_Date)


#t = Treasure(name ='Gold Nugget', value=500.00, material='gold', location="Curly's Creak, NM", image='https://png.pngtree.com/element_pic/17/08/30/62b817ced2917aef3fc27401635e31c6.jpg')
#
# DHT22 Results:
# Temp=19.8*  Humidity=71.5%
# BMP280 Results:
# Temperature : 20.26C
# Pressure : 964.956491117 hPa
# BH1750 Results:
# Light level: 6.66666666667lx
