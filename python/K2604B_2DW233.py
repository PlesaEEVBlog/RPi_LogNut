#!/usr/bin/python2
# Test Agilent E5810A
import vxi11
import Gpib
import os.path
import sys
import time


inst = vxi11.Instrument("192.168.0.27", "gpib0,29")
inst.write("*IDN?")
print(inst.read())

# SMU Assigment
smuX = 'smua'
smuY = 'smub'

LogDir = '/pub/logs/'
LogFile = LogDir + '2DW233_Log.csv'

# SMU Reset
inst.write("reset()")

SMU = smuX
# SMU Configuration
inst.write("smua.source.func = smua.OUTPUT_DCAMPS")
inst.write("smua.source.leveli = 0")
inst.write("smua.source.limitv = 10")
inst.write("smua.source.limiti = 0.010")
inst.write("smua.measure.rangev = 6")
inst.write("smua.measure.nplc = 25")
inst.write("display.smua.digits = display.DIGITS_6_5")
inst.write("smua.source.output = smua.OUTPUT_ON")


inst.write("smub.source.func = smub.OUTPUT_DCAMPS")
inst.write("smub.source.leveli = 0")
inst.write("smub.source.limitv = 10")
inst.write("smub.source.limiti = 0.010")
inst.write("smub.measure.rangev = 6")
inst.write("smub.measure.nplc = 25")
inst.write("display.smub.digits = display.DIGITS_6_5")
inst.write("smub.source.output = smub.OUTPUT_ON")


inst.write("display.clear()")
inst.write("display.setcursor(1, 1, 0)")
inst.write("display.settext('')")
inst.write("display.setcursor(2, 6, 0)")
inst.write("display.settext('')")

# Check file presence, write header
if (os.path.isfile(LogFile) == False):
  with open(LogFile, 'a') as EnvLog:
    EnvLog.write("TimeStamp,SMU A Current,SMU A Voltage,SMU B Current,SMU B Voltage\r\n")
    print ("File %s does not exist\r\n" % LogFile) 
try:
	while True:
		with open(LogFile, 'a') as EnvLog:
			inst.write("smua.source.leveli = -0.001")
			inst.write("print(smua.measure.v())")
			dataSMUX_V = inst.read()
			inst.write("print(smua.measure.i())")
			dataSMUX_I = inst.read()
			inst.write("smub.source.leveli = -0.001")
			inst.write("print(smub.measure.v())")
			dataSMUY_V = inst.read()
			inst.write("print(smub.measure.i())")
			dataSMUY_I = inst.read()
			print time.strftime("%d/%m/%Y\t%H:%M:%S") + ("\tSMU A I: %.6f\t SMU A V: %.6f\tSMU B I: %.6f\t SMU B V: %.6f\r" % (float(dataSMUX_I),float(dataSMUX_V),float(dataSMUY_I),float(dataSMUY_V)))
			EnvLog.write (time.strftime("%d/%m/%Y-%H:%M:%S,") + ("%f,%f,%f,%f\r\n"  % (float(dataSMUX_I),float(dataSMUX_V),float(dataSMUY_I),float(dataSMUY_V))))
			time.sleep(1)
except KeyboardInterrupt:
	inst.write("smua.source.output = smua.OUTPUT_OFF")
  	inst.write("smub.source.output = smub.OUTPUT_OFF")




