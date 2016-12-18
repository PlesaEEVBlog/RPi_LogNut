# Rigol DM3068 Multi Meter Python Measurement Script

# Import the libraries for the Rigol DM3068 Multi Meter. 
import usbtmc
import vxi11
import serial
import Gpib
import os.path
import sys
import time
from BME280 import *

LogDir = '/pub/logs/'
LogFile= LogDir + 'DM3068_Log.csv'
Reflevel = 16.800000000

# Sensors
BME_Enabled = 0
if (BME_Enabled == 1):
  BMEsensor = BME280(address=0x76)

# Rigol DM3068 Lan Connection
inst = vxi11.Instrument("192.168.1.201")
inst.clear()

# Rigol DM3068 USB Connection
#inst = usbtmc.Instrument("USB::0x1ab1::0x0c94::INSTR")
#inst.clear()

# Rigol DM3068 GPIB Connection
# inst = Gpib.Gpib(0,7)
# inst.clear()


# Rigol DM3068 Serial Port Connection
# ser = serial.Serial(
#		port='/dev/serial1',
#		baudrate = 115200,
#		parity=serial.PARITY_NONE,
#		stopbits=serial.STOPBITS_ONE,
#		bytesize=serial.EIGHTBITS,
#		timeout=1
#)
#
# ser.write("*IDN?\n")
# time.sleep(2)
# bytesToRead = ser.inWaiting()
# print ser.read(bytesToRead)
#
# ser.close()

# Setup Rigol DM3068 Meter for all types of measurements
inst.write("*CLS")
inst.write("SYSTem:DISPlay:BRIGht 32")
inst.write("[SENSe:]ZERO:AUTO ON")
inst.write('DISPlay:TEXT "Logging On!"')
inst.write("SYSTem:BEEPer:STATe ON")
inst.write("SYSTem:BEEPer")
inst.write("SYSTem:BEEPer:STATe OFF")

# DC Voltage Measurement
inst.write(":FUNCtion:VOLTage:DC")
inst.write("CONFigure:VOLTage:DC 20 V")
measurementvalue = ":MEASure:VOLTage:DC?"

# AC Voltage Measurement
# inst.write(":FUNCtion:VOLTage:AC")
# inst.write("CONFigure:VOLTage:AC 20 V")
# measurementvalue = ":MEASure:VOLTage:AC?"

# 2 Wire Ohms Resistence Measurement
# inst.write(":FUNCtion:RESistance")
# inst.write("CONFigure:RESistance 20000")
# measurementvalue = ":MEASure:RESistance?"

# 4 Wire Ohms Resistence Measurement
# inst.write(":FUNCtion:FRESistance")
# inst.write("CONFigure:FRESistance 20000")
# measurementvalue = ":MEASure:FRESistance?"

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
      data = inst.ask(measurementvalue)
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
