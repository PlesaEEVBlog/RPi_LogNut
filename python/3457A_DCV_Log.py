#!/usr/bin/python2
# Keithley 2001 log test
import Gpib
import os.path
import sys
import time
from BME280 import *

LogDir = '/pub/logs/'
LogFile= LogDir + '3457A_DCV_Log.csv'

# Sensors
BME_Enabled = 0
if (BME_Enabled == 1):
  BMEsensor = BME280(address=0x76)

Reflevel = 7.16733470
ppm = 0

# 3457A Address
inst = Gpib.Gpib(0,30)
inst.write("END ALWAYS")
inst.clear()  
inst.write("ID?")
print(inst.read())

# Setup 3457A
inst.write("CALNUM?")
print("Calibrated %s times" %inst.read())
inst.write("NPLC 100")
inst.write("FUNC DCV,30")
inst.write("TRIG HOLD")
inst.write("RMATH HIRES")
inst.write("MFORMAT ASCII")

# Check file presence, write header
if (os.path.isfile(LogFile) == False):
  with open(LogFile, 'a') as MeterLog:
    if (BME_Enabled == 1):
      MeterLog.write("TimeStamp,Voltage,ppm,Temperature,Pressure,Humidity\r\n")
    else:
      MeterLog.write("TimeStamp,Voltage,ppm\r\n")
    MeterLog.close()

while True:
    with open(LogFile, 'a') as MeterLog:
      inst.write("TRIG SGL")
      data = inst.read()
      ppm = ((float(data) / Reflevel)-1)*1E6
      if (BME_Enabled == 1):
         # Reads sensor data
         Temperature = BMEsensor.read_temperature()
         Pressure = BMEsensor.read_pressure()
         Humidity = BMEsensor.read_humidity()
         print time.strftime("%d/%m/%Y\t%H:%M:%S") + ("\t%.5f\t%.1f ppm\t%4.2f\t%6.0f\t%4.1f\r\n" % (float(data),float(ppm),float(Temperature),float(Pressure),float(Humidity)) )
         MeterLog.write (time.strftime("%d/%m/%Y-%H:%M:%S,") + ("%.5f,%.1f\r\n" % (float(data),float(ppm),float(Temperature),float(Pressure),float(Humidity))))
      else:
        print time.strftime("%d/%m/%Y\t%H:%M:%S") + ("\t%.5f\t%.1f ppm" % (float(data),float(ppm) ) )
        MeterLog.write (time.strftime("%d/%m/%Y-%H:%M:%S,") + ("%.5f,%.1f\r\n" % (float(data),float(ppm) ) ))
MeterLog.close()