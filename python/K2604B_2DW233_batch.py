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


BatchSize = 3
# SMU Assigment
smuX = 'smua'
smuY = 'smub'

LogDir = '/pub/logs/'
LogFile = LogDir + '2DW233_Log'

Test_Current = [-1E-6,-10E-6,-10E-6,-100E-6,-1E-3,-10E-3]

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


for Count in range (1,BatchSize+1):
	Count = Count + 1
	LogFileName = LogFile + '_' + str(Count) + '.csv'
	
	
	
	for TestCount in range (0,len(Test_Current)):
	# Check file presence, write header
		if (os.path.isfile(LogFileName) == False):
			with open(LogFileName, 'a') as EnvLog:
				EnvLog.write("TimeStamp,SMU_A_Current,SMU_A_Voltage,SMU_B_Current,SMU_B_Voltage\r\n")
				print ("File %s does not exist\r\n" % LogFileName) 
		with open(LogFileName, 'a') as EnvLog:
			inst.write("smua.source.leveli = %.9f" %Test_Current[TestCount])
			inst.write("print(smua.measure.v())")
			dataSMUX_V = inst.read()
			inst.write("print(smua.measure.i())")
			dataSMUX_I = inst.read()
			inst.write("smub.source.leveli = %.9f" %Test_Current[TestCount])
			inst.write("print(smub.measure.v())")
			dataSMUY_V = inst.read()
			inst.write("print(smub.measure.i())")
			dataSMUY_I = inst.read()
			print time.strftime("%d/%m/%Y\t%H:%M:%S") + ("\tSMU A I: %.6f\t SMU A V: %.6f\tSMU B I: %.6f\t SMU B V: %.6f\r" % (float(dataSMUX_I),float(dataSMUX_V),float(dataSMUY_I),float(dataSMUY_V)))
			EnvLog.write (time.strftime("%d/%m/%Y-%H:%M:%S,") + ("%f,%f,%f,%f\r\n"  % (float(dataSMUX_I),float(dataSMUX_V),float(dataSMUY_I),float(dataSMUY_V))))
			TestCount = TestCount + 1
			time.sleep(1)
	inst.write("smua.source.output = smua.OUTPUT_OFF")
	inst.write("smub.source.output = smub.OUTPUT_OFF")
	raw_input("Press Enter to continue...")