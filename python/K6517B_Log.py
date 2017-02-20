#!/usr/bin/python2
# Test Keithley 6517B

import Gpib
import vxi11
import os.path
import sys
import time
from si_prefix import si_format
from BME280 import *

LogDir = '/pub/logs/'
LogFile= LogDir + 'K6517B_Log.csv'
Reflevel = 10E6

# Sensors
BME_Enabled = 1
if (BME_Enabled == 1):
  BMEsensor = BME280(address=0x76)

# GPIB
# inst = Gpib.Gpib(0,27)

# GPIB LAN
inst = vxi11.Instrument("192.168.0.27", "gpib0,27")

inst.clear()
inst.write("*IDN?")
print(inst.read())

#Setup Keithley 6517B

inst.write("*CLS")
print("*CLS")
time.sleep(1)
inst.write(":ABORt")
print(":ABORt")
time.sleep(1)
inst.write(":SYSTem:PRESet")
print(":SYSTem:PRESet")
time.sleep(1)
inst.write("*RST")
print("*RST")
time.sleep(1)
inst.write(":INIT:CONT ON")
print(":INIT:CONT ON")
time.sleep(1)
inst.write(":DISPlay:ENABle OFF")
print(":DISPlay:ENABle OFF")
time.sleep(1)
inst.write(":FUNCtion 'CURRent:DC'")
print(":FUNCtion 'CURRent:DC'")
time.sleep(1)
inst.write(":CURRent:DC:RANGE:AUTO ON")
print(":CURRent:DC:RANGE:AUTO ON")
time.sleep(1)
inst.write(":CURRent:DC:NPLC 10")
print(":CURRent:DC:NPLC 10")
time.sleep(1)
inst.write(":CURRent:DC:AVERage:COUNt 100")
print(":CURRent:DC:AVERage:COUNt 100")
time.sleep(1)
inst.write(":CURRent:DC:AVERage:TCONtrol MOVing")
print(":CURRent:DC:AVERage:TCONtrol MOVing")
time.sleep(1)
inst.write(":SOURce:VOLTage:RANGe 100")
print(":SOURce:VOLTage:RANGe 100")
time.sleep(1)
inst.write(":SOURce:VOLTage 100")
print(":SOURce:VOLTage 100")
time.sleep(1)
inst.write(":SOURce:VOLTage:MCON ON")
print(":SOURce:VOLTage:MCON ON")
time.sleep(1)
inst.write(":SYSTem:ZCHeck OFF")
print(":SYSTem:ZCHeck OFF")
time.sleep(1)
inst.write(":OUTPut ON")
print(":OUTPut ON")

#Check file presence, write header
if (os.path.isfile(LogFile) == False):
  with open(LogFile, 'a') as MeterLog:
    if (BME_Enabled == 1):
      MeterLog.write("TimeStamp,Current,Temperature,Pressure,Humidity\r\n")
    else:
      MeterLog.write("TimeStamp,Current\r\n")
    MeterLog.close()

while True:
    with open(LogFile, 'a') as MeterLog:
      #inst.write("READ?")
      #data = inst.read()
      #ppm = ((float(data) / Reflevel)-1)*1E6
      inst.write(":FETCH?")
      dataRaw = inst.read()
      Readout =dataRaw.split("NADC,")
      data = Readout[0]
      if (BME_Enabled == 1):
         # Reads sensor data
         Temperature = BMEsensor.read_temperature()
         Pressure = BMEsensor.read_pressure()
         Humidity = BMEsensor.read_humidity()
         print time.strftime("%d/%m/%Y\t%H:%M:%S") + ("\t%.17f\t%sA\tTemperature: %4.2f C\tPressure: %6.0f Pa\tRh: %4.1f" %(float(data),si_format(float(data),precision=2),float(Temperature),float(Pressure),float(Humidity)))
         MeterLog.write (time.strftime("%d/%m/%Y-%H:%M:%S,") + ("%.17f,%4.2f,%6.0f,%4.1f\r\n" %(float(data),float(Temperature),float(Pressure),float(Humidity))))
      else:
        print time.strftime("%d/%m/%Y\t%H:%M:%S") + ("\t%.17f\t%sA" %(float(data),si_format(float(data), precision=2)))
        MeterLog.write (time.strftime("%d/%m/%Y-%H:%M:%S,") + ("%.17f\r\n" %float(data)))
      time.sleep(1)
MeterLog.close()
