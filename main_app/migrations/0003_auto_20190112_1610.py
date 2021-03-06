# Generated by Django 2.1.5 on 2019-01-12 16:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_measurements_room_humidity'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurements',
            name='room_Light',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='measurements',
            name='room_Pressure',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='measurements',
            name='room_Date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
