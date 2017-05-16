# Keysight U1272A Multi Meter

import serial
import os.path
import sys
import time
from BME280 import *

LogDir = '/pub/logs/'
LogFile= LogDir + 'U1272A_Log.csv'
Reflevel = 4.21000000

# Sensors
BME_Enabled = 0
if (BME_Enabled == 1):
  BMEsensor = BME280(address=0x76)

ser = serial.Serial(
		port='/dev/ttyUSB0',
		baudrate = 19200,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=0.5
)

def send_receive(command):
    ser.write(command + '\n')
    time.sleep(0.02)
    received = ser.read(100)
    received = received.replace('\n','')
    return received

# Setup the Keysight U1272A Meter
# send_receive("*RST")
send_receive("CONF:VOLT:DC")
send_receive('*IDN?')
time.sleep(0.1)

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
      data = send_receive('FETC?')
      ppm = ((float(data) / Reflevel)-1)*1E6
      if (BME_Enabled == 1):
         # Reads sensor data
         Temperature = BMEsensor.read_temperature()
         Pressure = BMEsensor.read_pressure()
         Humidity = BMEsensor.read_humidity()
         print time.strftime("%d/%m/%Y\t%H:%M:%S") + ("\t%.8f\t%.1f ppm\t%4.2f\t%6.0f\t%4.1f\r\n" % (float(data),float(ppm),float(Temperature),float(Pressure),float(Humidity)))
         MeterLog.write (time.strftime("%d/%m/%Y-%H:%M:%S,") + ("%.8f,%.1f,%4.2f,%6.0f,%4.1f\r\n" % (float(data),float(ppm),float(Temperature),float(Pressure),float(Humidity))))
      else:
        print time.strftime("%d/%m/%Y\t%H:%M:%S") + ("\t%.8f\t%.1f ppm" % (float(data),float(ppm) ) )
        MeterLog.write (time.strftime("%d/%m/%Y-%H:%M:%S,") + ("%.8f,%.1f\r\n" % (float(data),float(ppm) ) ))
        MeterLog.close()
ser.close()
