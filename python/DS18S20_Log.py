#!/usr/bin/python2
# Python Dual BME280 logging script
import os.path
import sys
import time
import numbers
import signal

LogDir = '/pub/logs/'
LogFile = LogDir + 'DS18S20_Log.csv'

# Sensors 
#Sensor_Address = '28-0316642118ff' 
Sensor_Address = '28-041663de08ff'

# Check file presence, write header
if (os.path.isfile(LogFile) == False):
  with open(LogFile, 'a') as EnvLog:
    EnvLog.write("TimeStamp,Temperature\r\n")
    print ("File %s does not exist\r\n" % LogFile) 

try:
  #Setup temp/humidity/pressure sensor BME280
  while True:
    # Reads sensor data
    Sensor = open("/sys/bus/w1/devices/%s/w1_slave" %Sensor_Address)
    Readout = Sensor.read()
    Sensor.close()
    RawTemperature = Readout.split("\n")[1].split(" ")[9]
    Temperature = float(RawTemperature[2:])/1000
    
    print time.strftime("%d/%m/%Y\t%H:%M:%S") + ("\tTemperature: %4.3f C" % (float(Temperature) ) )
    with open(LogFile, 'a') as EnvLog:
      EnvLog.write (time.strftime("%d/%m/%Y-%H:%M:%S,") + ("%4.3f\r\n" % (float(Temperature) ) ) )
      EnvLog.close()
    time.sleep(10)
    
except KeyboardInterrupt:
	pass    
