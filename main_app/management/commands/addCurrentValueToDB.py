#from .models import Measurements
from django.core.management.base import BaseCommand
from main_app.models import Measurements
from main_app.WeatherStation import main
import time

class Command(BaseCommand):
    def handle(self, **options):
        temperature_list=[]
        humidity_list=[]
        pressure_list=[]
        light_list=[]
        while True:
            t_end = time.time() + 60 * 5
            while t_end > time.time():
                temperature,humidity,pressure,light = main()
                temperature_list.append(temperature)
                humidity_list.append(humidity)
                pressure_list.append(pressure)
                light_list.append(light)
                time.sleep(2)
            measurement = Measurements(room_Temperature=sorted(temperature_list,reverse=True)[int(len(temperature_list)*0.95-1)], #Get 5% lowest value
                                        room_Humidity=sorted(humidity_list,reverse=True)[int(len(humidity_list)*0.95-1)], #Get 5% lowest value
                                        room_Pressure=sorted(pressure_list,reverse=True)[int(len(pressure_list)*0.95-1)], #Get 5% lowest value
                                        room_Light=sorted(light_list,reverse=True)[int(len(light_list)*0.95-1)]) #Get 5% highest value
            measurement.save()
            temperature_list.clear()
            humidity_list.clear()
            pressure_list.clear()
            light_list.clear()
            #time.sleep(1)
#post_currentValues(22.5,90,1000,110)
#python3 manage.py shell <<EOF\ execfile('main_app/Test_WeatherStation.py') \EOF
# echo 'import Test_WeatherStation.py' | python3 ../manage.py shell
