import smbus
import Adafruit_DHT
import time
from ctypes import c_short
from ctypes import c_byte
from ctypes import c_ubyte

DEVICE_BMP280 = 0x76 # Default device I2C address
DEVICE_BH1750 = 0x23 # Default device I2C address

#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi, Pi 2 & Pi 3 uses bus 1
                     # Rev 1 Pi uses bus 0

# Define some constants from the datasheet

POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value

# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23

def readDHT22():
    sensor = Adafruit_DHT.DHT22
    pin = 4
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    return humidity,temperature

def getShort(data, index):
	# return two bytes from data as a signed 16-bit value
	return c_short((data[index+1] << 8) + data[index]).value

def getUShort(data, index):
	# return two bytes from data as an unsigned 16-bit value
	return (data[index+1] << 8) + data[index]

def getChar(data,index):
	# return one byte from data as a signed char
	result = data[index]
	if result > 127:
		result -= 256
	return result

def getUChar(data,index):
	# return one byte from data as an unsigned char
	result =  data[index] & 0xFF
	return result

def readBMP280All(addr=DEVICE_BMP280):
	# Register Addresses
	REG_DATA = 0xF7
	REG_CONTROL = 0xF4
	REG_CONFIG  = 0xF5

	REG_HUM_MSB = 0xFD
	REG_HUM_LSB = 0xFE

	# Oversample setting - page 27
	OVERSAMPLE_TEMP = 2
	OVERSAMPLE_PRES = 2
	MODE = 1

	control = OVERSAMPLE_TEMP<<5 | OVERSAMPLE_PRES<<2 | MODE
	bus.write_byte_data(addr, REG_CONTROL, control)

	# Read blocks of calibration data from EEPROM
	# See Page 22 data sheet
	cal1 = bus.read_i2c_block_data(addr, 0x88, 24)
	cal2 = bus.read_i2c_block_data(addr, 0xA1, 1)
	cal3 = bus.read_i2c_block_data(addr, 0xE1, 7)

	# Convert byte data to word values
	dig_T1 = getUShort(cal1, 0)
	dig_T2 = getShort(cal1, 2)
	dig_T3 = getShort(cal1, 4)

	dig_P1 = getUShort(cal1, 6)
	dig_P2 = getShort(cal1, 8)
	dig_P3 = getShort(cal1, 10)
	dig_P4 = getShort(cal1, 12)
	dig_P5 = getShort(cal1, 14)
	dig_P6 = getShort(cal1, 16)
	dig_P7 = getShort(cal1, 18)
	dig_P8 = getShort(cal1, 20)
	dig_P9 = getShort(cal1, 22)

	dig_H1 = getUChar(cal2, 0)
	dig_H2 = getShort(cal3, 0)
	dig_H3 = getUChar(cal3, 2)

	dig_H4 = getChar(cal3, 3)
	dig_H4 = (dig_H4 << 24) >> 20
	dig_H4 = dig_H4 | (getChar(cal3, 4) & 0x0F)

	dig_H5 = getChar(cal3, 5)
	dig_H5 = (dig_H5 << 24) >> 20
	dig_H5 = dig_H5 | (getUChar(cal3, 4) >> 4 & 0x0F)

	dig_H6 = getChar(cal3, 6)

	# Read temperature/pressure
	data = bus.read_i2c_block_data(addr, REG_DATA, 8)
	pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
	temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)

	#Refine temperature
	var1 = ((((temp_raw>>3)-(dig_T1<<1)))*(dig_T2)) >> 11
	var2 = (((((temp_raw>>4) - (dig_T1)) * ((temp_raw>>4) - (dig_T1))) >> 12) * (dig_T3)) >> 14
	t_fine = var1+var2
	temperature = float(((t_fine * 5) + 128) >> 8);

	# Refine pressure and adjust for temperature
	var1 = t_fine / 2.0 - 64000.0
	var2 = var1 * var1 * dig_P6 / 32768.0
	var2 = var2 + var1 * dig_P5 * 2.0
	var2 = var2 / 4.0 + dig_P4 * 65536.0
	var1 = (dig_P3 * var1 * var1 / 524288.0 + dig_P2 * var1) / 524288.0
	var1 = (1.0 + var1 / 32768.0) * dig_P1
	if var1 == 0:
		pressure=0
	else:
		pressure = 1048576.0 - pres_raw
		pressure = ((pressure - var2 / 4096.0) * 6250.0) / var1
		var1 = dig_P9 * pressure * pressure / 2147483648.0
		var2 = pressure * dig_P8 / 32768.0
		pressure = pressure + (var1 + var2 + dig_P7) / 16.0

	return temperature/100.0,pressure/100.0

def convertToNumber(data):
	# Simple function to convert 2 bytes of data
	# into a decimal number
	return ((data[1] + (256 * data[0])) / 1.2)

def readLight(addr=DEVICE_BH1750):
	data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
	return convertToNumber(data)

def main():
    #while True:
    # temperature=0.0
    # humidity=0.0
    # pressure=0.0
    # light=0.0
    #for x in range(7):
    humidity, temperature = readDHT22()
        #print('DHT22 Results:')
        #print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
    temperature,pressure = readBMP280All()
        # print('BMP280 Results:')
        # print('Temperature : {0}C'.format(temperature))
        # print("Pressure : {0} hPa".format(pressure))
    light = readLight()
        # print('BH1750 Results:')
        # print('Light level: {0}lx'.format(light))
    #time.sleep(0.5)
    return temperature,humidity,pressure,light

if __name__=="__main__":
   main()
