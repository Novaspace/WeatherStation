# Generated by Django 2.1.5 on 2019-01-12 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_auto_20190112_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurements',
            name='room_Light',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
    ]