#!/usr/bin/python2
# Python Dual BME280 logging script
import os.path
import sys
import time
import numbers
import signal

LogDir = '/pub/logs/'
LogFile = LogDir + 'DS18S20_Dual_Log.csv'

# Sensors 
#Sensor_Address = '28-0316642118ff' 
#Sensor_Address = '28-041663de08ff'
Sensor_A_Address = '28-03166341f1ff'
Sensor_B_Address = '28-041662b8d2ff'


# Check file presence, write header
if (os.path.isfile(LogFile) == False):
  with open(LogFile, 'a') as EnvLog:
    EnvLog.write("TimeStamp,Temperature\r\n")
    print ("File %s does not exist\r\n" % LogFile) 

try:
  #Setup temp/humidity/pressure sensor BME280
  while True:
    # Reads sensor data
    SensorA = open("/sys/bus/w1/devices/%s/w1_slave" %Sensor_A_Address)
    SensorB = open("/sys/bus/w1/devices/%s/w1_slave" %Sensor_B_Address)
    ReadoutA = SensorA.read()
    ReadoutB = SensorB.read()
    SensorA.close()
    SensorB.close()
    RawTemperatureA = ReadoutA.split("\n")[1].split(" ")[9]
    TemperatureA = float(RawTemperatureA[2:])/1000
    RawTemperatureB = ReadoutB.split("\n")[1].split(" ")[9]
    TemperatureB = float(RawTemperatureB[2:])/1000
        
    print time.strftime("%d/%m/%Y\t%H:%M:%S") + ("\tTemperature: %4.3f C\t%4.3f" % (float(TemperatureA),float(TemperatureB)) )
    with open(LogFile, 'a') as EnvLog:
      EnvLog.write (time.strftime("%d/%m/%Y-%H:%M:%S,") + ("%4.3f\t%4.3f\r\n" % (float(TemperatureA),float(TemperatureB))))
      EnvLog.close()
    time.sleep(1)
    
except KeyboardInterrupt:
	pass    
