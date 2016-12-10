# Test Agilent 34411A
import usbtmc
import os.path
import sys
import time
from BME280 import *

LogDir = '/pub/logs/'
LogFile= LogDir + '34411A_Log.csv'
Reflevel = 7.167343414

# Sensors
BME_Enabled = 0
if (BME_Enabled == 1):
  BMEsensor = BME280(address=0x76)

#34411A
inst =  usbtmc.Instrument("USB::0x0957::0x0a07::INSTR")
#34410A
#inst =  usbtmc.Instrument("USB::0x0957::0x0607::INSTR")

print(inst.ask("*IDN?"))
inst.clear()

#Setup Agilent 34411A
inst.write("*RST")
inst.write("SYST:PRES")
inst.write("*CLS")
inst.write("FORM:DATA ASCii,9")

# DCV 
inst.write("FUNC 'VOLT:DC'")
inst.write("VOLT:DC:RANG 10")
inst.write("VOLT:DC:NPLC 100")


# 4W Ohms
#inst.write("FUNC 'FRESistance'")
#inst.write("FRES:RANG 10000")
#inst.write("FRES:NPLC 100")

inst.write("VOLT:DC:IMP:AUTO OFF")
inst.write("VOLT:ZERO:AUTO OFF")
inst.write("VOLT:NULL:STAT OFF")
inst.write("CALC:STAT OFF")
inst.write("TRIG:SOUR IMM")
inst.write("TRIG:COUN 1")
inst.write("TRIG:DEL:AUTO OFF")
inst.write("DISP OFF")

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
      data = inst.ask("READ?")
      ppm = ((float(data) / Reflevel)-1)*1E6
      if (BME_Enabled == 1):
         # Reads sensor data
         Temperature = BMEsensor.read_temperature()
         Pressure = BMEsensor.read_pressure()
         Humidity = BMEsensor.read_humidity()
         print time.strftime("%d/%m/%Y\t%H:%M:%S") + ("\t%.8f\t%.1f ppm\t%4.2f\t%6.0f\t%4.1f\r\n" % (float(data),float(ppm),float(Temperature),float(Pressure),float(Humidity)) )
         MeterLog.write (time.strftime("%d/%m/%Y-%H:%M:%S,") + ("%.8f,%.1f,%4.2f,%6.0f,%4.1f\r\n" % (float(data),float(ppm),float(Temperature),float(Pressure),float(Humidity))))
      else:
        print time.strftime("%d/%m/%Y\t%H:%M:%S") + ("\t%.8f\t%.1f ppm" % (float(data),float(ppm) ) )
        MeterLog.write (time.strftime("%d/%m/%Y-%H:%M:%S,") + ("%.8f,%.1f\r\n" % (float(data),float(ppm) ) ))
MeterLog.close()
