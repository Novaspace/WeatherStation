# Generated by Django 2.1.5 on 2019-02-10 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_auto_20190112_1614'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='measurements',
            index=models.Index(fields=['room_Date'], name='main_app_me_room_Da_0bc272_idx'),
        ),
    ]