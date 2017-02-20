#!/usr/bin/python2
# Python script for logging 3458A ACAL 
import vxi11
import os.path
import sys
import Gpib
import time

# 3458A GPIB Address = 22
#inst = Gpib.Gpib(0,22, timeout=60) 

# 3458A Connect to E5810A

inst = vxi11.Instrument("192.168.0.27", "gpib0,22")

inst.clear()  
inst.write("ID?")
print(inst.read())

LogDir = '/pub/logs/'
LogFile= LogDir + '3458A_DCV_Log_complete.csv'
LogFile_ACAL= LogDir + '3458A_ACAL_DCV_Log.csv'

# Setup HP 3458A
inst.write("PRESET NORM")
inst.write("OFORMAT ASCII")
inst.write("END ALWAYS")

if (os.path.isfile(LogFile_ACAL) == False):
  with open(LogFile_ACAL, 'a') as ACALLog:
    ACALLog.write("TimeStamp,DCV_Gain,Temperature\r\n")
    ACALLog.close()
    
    
response = ''
FullResponse = []
for i in range(1, 253):
  inst.write("CAL? %d" % i)
  #print(inst.read())
  FullResponse.append(float(inst.read()))
  #FullResponse.append(response)
print response 
print FullResponse

#if (os.path.isfile(LogFile_ACAL) == False):
#  with open(LogFile_ACAL, 'a') as ACALLog:
#    ACALLog.write("TimeStamp,DCV_Gain,Temperature\r\n")
#    ACALLog.close() 
