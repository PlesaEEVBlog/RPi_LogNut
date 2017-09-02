# Keithley 2001 log test
import Gpib
import os.path
import sys
import time
from BME280 import *

LogDir = '/pub/logs/'
LogFile= LogDir + 'K2001_Log.csv'
Reflevel = 7.1258
# Sensors
BME_Enabled = 0
if (BME_Enabled == 1):
  BMEsensor = BME280(address=0x76)

Reflevel = 7.164971
ppm = 0

# K2001 address
inst = Gpib.Gpib(0,16)
inst.clear()  
inst.write("*IDN?")
print(inst.read())

# Setup K2001
inst.write("*RST")
inst.write("*CLR")
inst.write(":SYST:AZER:TYPE SYNC")
inst.write(":SYST:LSYN:STAT ON")
inst.write(":SENS:FUNC 'VOLT:DC'")
inst.write(":SENS:VOLT:DC:RANG 20")
inst.write(":SENS:VOLT:DC:DIG 9; NPLC 10; AVER:COUN 5; TCON REP")
inst.write(":FORM:ELEM READ")
inst.write(":DISP:WIND:TEXT:DATA \"               \";STAT ON;")
inst.write(":DISP:WIND2:TEXT:DATA \"               \";STAT ON;")


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
      inst.write("READ?")
      data = inst.read()
      ppm = ((float(data) / Reflevel)-1)*1E6
      if (BME_Enabled == 1):
         # Reads sensor data
         Temperature = BMEsensor.read_temperature()
         Pressure = BMEsensor.read_pressure()
         Humidity = BMEsensor.read_humidity()
         print time.strftime("%d/%m/%Y\t%H:%M:%S") + ("\t%.8f\t%.1f ppm\t%4.2f\t%6.0f\t%4.1f\r\n" % (float(data),float(ppm),float(Temperature),float(Pressure),float(Humidity)) )
         MeterLog.write (time.strftime("%d/%m/%Y-%H:%M:%S,") + ("%.8f,%.1f\r\n" % (float(data),float(ppm),float(Temperature),float(Pressure),float(Humidity))))
      else:
        print time.strftime("%d/%m/%Y\t%H:%M:%S") + ("\t%.8f\t%.1f ppm" % (float(data),float(ppm) ) )
        MeterLog.write (time.strftime("%d/%m/%Y-%H:%M:%S,") + ("%.8f,%.1f\r\n" % (float(data),float(ppm) ) ))
MeterLog.close()