#!/usr/bin/python2

# Test Agilent 34420A
import Gpib
import vxi11
import os.path
import sys
import time
from BME280 import *

LogDir = '/pub/logs/'
LogFile= LogDir + '34420A_Res_LogTemp_10k_UltraOhm.csv'
Reflevel = 10000

# Sensors
BME_Enabled = 1
if (BME_Enabled == 1):
  BMEsensor = BME280(address=0x77)

# 34420A GPIB
inst = Gpib.Gpib(0,20)
#34420A LAN
#inst = Gpib.Gpib(0,24)
# 34410A LAN
#inst = vxi11.Instrument("192.168.0.27", "gpib0,20")

inst.clear()  
inst.write("*IDN?")
print(inst.read())

#Setup Agilent 34420A
inst.write("*RST")
inst.write("SYST:PRES")
inst.write("*CLS")

# DCV 34401A/34420A
#inst.write(":CONFigure:VOLTage:DC 10")
#inst.write(":SENSe:VOLTage:DC:RANGe 10")
#inst.write(":SENSe:VOLTage:DC:NPLCycles 100")

# Ratio
#inst.write(":CONFigure:VOLTage:DC:RATio 10")
# 4W Ohms
inst.write(":CONFigure:FRESistance 10000")
inst.write(":SENSe:FRESistance:RANGe 10000")
inst.write(":SENSe:FRESistance:NPLCycles 100")

inst.write(":DISPlay OFF")

# Check file presence, write header
if (os.path.isfile(LogFile) == False):
  with open(LogFile, 'a') as MeterLog:
    if (BME_Enabled == 1):
      MeterLog.write("TimeStamp,Resistance,ppm,Temperature,Pressure,Humidity\r\n")
    else:
      MeterLog.write("TimeStamp,Resistance,ppm\r\n")
    MeterLog.close()

while True:
    with open(LogFile, 'a') as MeterLog:
      inst.write("READ?")
      data = inst.read()
      ppm = ((float(data) / Reflevel)-1)*1E6
      if (BME_Enabled == 1):
         # Reads sensor data
         Temperature = BMEsensor.read_temperature()
         Pressure = BMEsensor.read_pressure()
         Humidity = BMEsensor.read_humidity()
         print time.strftime("%d/%m/%Y\t%H:%M:%S") + ("\t%.8f\t%.2f ppm\t%4.2f\t%6.0f\t%4.1f\r\n" % (float(data),float(ppm),float(Temperature),float(Pressure),float(Humidity)) )
         MeterLog.write (time.strftime("%d/%m/%Y-%H:%M:%S,") + ("%.8f,%.2f,%4.2f,%6.0f,%4.1f\r\n" % (float(data),float(ppm),float(Temperature),float(Pressure),float(Humidity))))
      else:
        print time.strftime("%d/%m/%Y\t%H:%M:%S") + ("\t%.8f\t%.2f ppm" % (float(data),float(ppm) ) )
        MeterLog.write (time.strftime("%d/%m/%Y-%H:%M:%S,") + ("%.8f,%.2f\r\n" % (float(data),float(ppm) ) ))
MeterLog.close()
