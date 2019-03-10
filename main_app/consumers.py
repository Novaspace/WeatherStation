import json
import asyncio
import datetime
from decimal import Decimal
from channels.consumer import AsyncConsumer
from .models import Measurements

class GaugeConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })

        while True:
            await asyncio.sleep(2)

            #obj = # do_something (Ex: constantly query DB...)
            last_measurement = Measurements.objects.last()
            myObj = {'time': last_measurement.room_Date,
                'temperature': last_measurement.room_Temperature,
                'humidity': last_measurement.room_Humidity,
                'pressure': last_measurement.room_Pressure,
                'light': last_measurement.room_Light}
            #json_obj = {'last_measurement' : last_measurement.room_Temperature,}
            date_handler = lambda obj: (
            obj.isoformat()
            if isinstance(obj, (datetime.datetime, datetime.date))
            else str(obj).__str__()
             #else json.JSONEncoder().default(obj)
            )
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps(myObj, indent=4, sort_keys=True, default=date_handler)#"{}".format(last_measurement.room_Temperature) # obj,
            })

    async def websocket_receive(self, event):
        print("receive", event)

    async def websocket_disconnect(self, event):
        #the code below is necessary in order to avoid the warning related to "..took too long to shut down.."
        if self.sock:
            self.sock.close()
        print("disconnected", event)
