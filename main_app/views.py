# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import Measurements
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.cache import cache_page

import json
import ujson
import datetime
import logging
from ctypes import cdll
# from .fooWrapper import *

# Create your views here.
logger = logging.getLogger(__name__)

def room(request):
    last_measurement = Measurements.objects.last()
    time_threshold = datetime.datetime.now()- datetime.timedelta(days=1)
    measurements = Measurements.objects.filter(room_Date__gte=time_threshold)

    return render(request, 'room.html', {'last_measurement' : last_measurement,
                                        'measurements' : measurements})

def lastMonthTH(request):
    time_threshold = datetime.datetime.now()- datetime.timedelta(days=30)
    #data = Measurements.objects.filter(room_Date__gte=time_threshold)
    #logging.error("++++ befor Querry ++++")
    dataset = Measurements.objects.filter(room_Date__gte=time_threshold).values('room_Date', 'room_Temperature', 'room_Humidity')
    #logging.error("++++ after Querry ++++")
    #data_json = json.dumps(list(data2),cls=DjangoJSONEncoder) #ujson.dumps(list(data2))
    #logging.error("++++ after json_dumps ++++")

    #return JsonResponse(data_json, safe=False)
    chart = {
    'xAxis': {
        'categories': list(map(lambda row: row['room_Date'].strftime('%d, %X'),dataset))
    },
    'series': [{
        'data': list(map(lambda row: {'y': row['room_Temperature']},dataset))
    },
    {
        'data': list(map(lambda row: {'y': row['room_Humidity']},dataset)),
        "yAxis":1
    }]
    }
    return JsonResponse(chart)

@cache_page(60 * 5)
def lastMonth(request):
    time_threshold = datetime.datetime.now()- datetime.timedelta(days=30)
    dataset = Measurements.objects.filter(room_Date__gte=time_threshold).values('room_Date','room_Temperature', 'room_Humidity', 'room_Pressure', 'room_Light')
    if "lastMonthPL" in str(request):
        chart = {
        'xAxis': {
            'categories': list(map(lambda row: row['room_Date'].strftime('%d, %X'),dataset))
        },
        'series': [{
            'data': list(map(lambda row: {'y': row['room_Pressure']},dataset))
        },
        {
            'data': list(map(lambda row: {'y': row['room_Light']},dataset)),
            "yAxis":1
        }]
        }
    elif 'lastMonthTH' in str(request):
        chart = {
        'xAxis': {
            'categories': list(map(lambda row: row['room_Date'].strftime('%d, %X'),dataset))
        },
        'series': [{
            'data': list(map(lambda row: {'y': row['room_Temperature']},dataset))
        },
        {
            'data': list(map(lambda row: {'y': row['room_Humidity']},dataset)),
            "yAxis":1
        }]
        }

    return JsonResponse(chart)
