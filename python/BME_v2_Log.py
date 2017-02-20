#!/usr/bin/python2
# Python Dual BME280 logging script
import os.path
import sys
import time
import numbers
import signal
from BME280 import *

LogDir = '/pub/logs/'
LogFile = LogDir + 'BME280_Log.csv'

# Sensors 
try:
    sensorA = BME280(address=0x76)
    BME_A_Present = True
except IOError as e:
    print "I/O error({0}): {1} when initializing BME280 Sensor 0".format(e.errno, e.strerror)
    BME_A_Present = False
try:
    sensorB = BME280(address=0x77)
    BME_B_Present = True
except IOError as e:
    print "I/O error({0}): {1} when initializing BME280 Sensor 1".format(e.errno, e.strerror)
    BME_B_Present = False
    
# Reads sensor data
if (BME_A_Present):
    BME_A_Temperature = sensorA.read_temperature()
    BME_A_Pressure = sensorA.read_pressure()
    BME_A_Humidity = sensorA.read_humidity()
else:
    BME_A_Temperature = 25
    BME_A_Pressure = 101000
    BME_A_Humidity = 40

if (BME_B_Present):
    BME_B_Temperature = sensorB.read_temperature()
    BME_B_Pressure = sensorB.read_pressure()
    BME_B_Humidity = sensorB.read_humidity()
else:
    BME_B_Temperature = 25
    BME_B_Pressure = 101000
    BME_B_Humidity = 40

#print 'Timestamp = {0:0.3f}'.format(sensor.t_fine)
#print 'A Temp      = {0:0.2f} deg C'.format(degreesA)
#print 'A Pressure  = {0:0.0f} Pa'.format(pascalsA)
#print 'A Humidity  = {0:0.1f} %'.format(humidityA)
#print 'B Temp      = {0:0.2f} deg C'.format(degreesB)
#print 'B Pressure  = {0:0.0f} Pa'.format(pascalsB)
#print 'B Humidity  = {0:0.1f} %'.format(humidityB)

# Check file presence, write header
if (os.path.isfile(LogFile) == False):
  with open(LogFile, 'a') as EnvLog:
    EnvLog.write("TimeStamp,BME_A_Temperature,BME_B_Temperature,BME_A_Pressure,BME_B_Pressure,BME_A_Humidity,BME_B_Humidity\r\n")
    print ("File %s does not exist\r\n" % LogFile) 

#Setup temp/humidity/pressure sensor BME280
while True:
    # Reads sensor data
    if (BME_A_Present):
        BME_A_Temperature = sensorA.read_temperature()
        BME_A_Pressure = sensorA.read_pressure()
        BME_A_Humidity = sensorA.read_humidity()
    else:
        BME_A_Temperature = 0
        BME_A_Pressure = 0
        BME_A_Humidity = 0

    if (BME_B_Present):
        BME_B_Temperature = sensorB.read_temperature()
        BME_B_Pressure = sensorB.read_pressure()
        BME_B_Humidity = sensorB.read_humidity()
    else:
        BME_B_Temperature = 0
        BME_B_Pressure = 0
        BME_B_Humidity = 0
        
    print time.strftime("%d/%m/%Y\t%H:%M:%S") + ("\tTemperature: %2.2f C %2.2f C\tPressure: %6.0f Pa %6.0f Pa\tRelative Humidity: %3.1f %3.1f" % (float(BME_A_Temperature),float(BME_B_Temperature),float(BME_A_Pressure),float(BME_B_Pressure),float(BME_A_Humidity),float(BME_B_Humidity) ) )
    with open(LogFile, 'a') as EnvLog:
      EnvLog.write (time.strftime("%d/%m/%Y-%H:%M:%S,") + ("%4.2f,%4.2f,%6.0f,%6.0f,%4.1f,%4.1f\r\n" % (float(BME_A_Temperature),float(BME_B_Temperature),float(BME_A_Pressure),float(BME_B_Pressure),float(BME_A_Humidity),float(BME_B_Humidity) ) ))
      EnvLog.close()
    time.sleep(10)
