#!/usr/bin/python2
# Python script for logging 3458A with automatic ACAL 
import vxi11
import os.path
import sys
import Gpib
import time

# 3458A GPIB Address = 22
inst = Gpib.Gpib(0,22, timeout=60) 

# 3458A Connect to E5810A

#inst = vxi11.Instrument("192.168.0.27", "gpib0,22")

inst.clear()  
inst.write("ID?")
print(inst.read())

LogDir = '/pub/logs/'
LogFile= LogDir + '3458A_DCV_Log.csv'
LogFile_ACAL= LogDir + '3458A_ACAL_DCV_Log.csv'

# Setup HP 3458A
inst.write("PRESET NORM")
inst.write("OFORMAT ASCII")
inst.write("DCV 10")
inst.write("TARM HOLD")
inst.write("TRIG AUTO")
inst.write("NPLC 200")
inst.write("AZERO ON")
inst.write("LFILTER ON")
inst.write("NRDGS 1,AUTO")
inst.write("MEM OFF")
inst.write("END ALWAYS")
inst.write("NDIG 9")
inst.write("DELAY 0")

# ACAL reference temperature
ACAL_Temperature = 39.2
ACAL_Counter = 0
# Perform ACAL if internal temperature differce is bigger than 1K
ACAL_Treshold = 1 	# every 1 deg C
ACAL_TimeInterval = 86400 # every 24h=86400

# LTZ boards reference values
#reflevel = 7.10616608
#4 reflevel = 7.137473141
reflevel = 7.16733470
#reflevel = 7.16508192 

ppm = 0
tread = 1
Last_ACAL_TimeStamp = 0
TempMeasurement_Interval = 500

# Check file presence, write header
if (os.path.isfile(LogFile) == False):
  with open(LogFile, 'a') as MeterLog:
    MeterLog.write("TimeStamp,Voltage,Temperature,ppm\r\n")
    MeterLog.close()
    
# Check ACAL file presence, write header
if (os.path.isfile(LogFile_ACAL) == False):
  with open(LogFile_ACAL, 'a') as ACALLog:
    ACALLog.write("TimeStamp,DCV_Gain,Temperature\r\n")
    ACALLog.close() 
    
while True:
  with open(LogFile, 'a') as MeterLog:
    tread = tread - 1
    if (tread == 0):
      tread = TempMeasurement_Interval
      #inst.write("TARM SGL,1")
      inst.write("TEMP?")
      Temperature = float(inst.read())
    if (abs(ACAL_Temperature - Temperature) >= ACAL_Treshold) or (time.time() - Last_ACAL_TimeStamp >= ACAL_TimeInterval):
        print('Temperature or time difference since last ACAL is higher than set treshold %.1f C / %d s') %(float(ACAL_Treshold),ACAL_TimeInterval)
        print('Since start ACAL performed %.0f times') %float(ACAL_Counter)
        print('Performing ACAL DCV, it will takes 3 minutes')
        ACAL_Counter+=1
        inst.write("ACAL DCV")
        Last_ACAL_TimeStamp = time.time()
        time.sleep(180)
        inst.write("CAL? 72")
        DCV10Gain = float(inst.read())
        print "10V Gain DCV = %.9f " %DCV10Gain
        print "Internal Temperature = %2.1f" %float(Temperature)
        ACAL_Temperature = Temperature
        with open(LogFile_ACAL, 'a') as ACALLog:
          ACALLog.write (time.strftime("%d/%m/%Y-%H:%M:%S,") + ("%.9f,%.2f\r\n" % (float(DCV10Gain),float(Temperature) ) ))
          ACALLog.close()
    inst.write("TARM SGL,1")
    data = inst.read()
    ppm = ((float(data) / reflevel)-1)*1E6
    inst.write("DISP OFF,\"  \"")
    print time.strftime("%d/%m/%Y\t%H:%M:%S") + ("\t%d x ACAL\t%.8f\t%.3f ppm\t%.1f C" % (ACAL_Counter, float(data),float(ppm),float(Temperature) ) )
    MeterLog.write (time.strftime("%d/%m/%Y-%H:%M:%S,") + ("%.8f,%.1f,%.3f\r\n" % (float(data),float(Temperature),float(ppm) ) ))
    MeterLog.close()
