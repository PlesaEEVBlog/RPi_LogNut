#!/usr/bin/python2
import vxi11
import Gpib
import os.path
import sys
import time
 
inst = vxi11.Instrument("192.168.0.27", "gpib0,29")
inst.write("*IDN?")
print(inst.read())

LogDir = '/pub/logs/'
LogFile = LogDir + 'PID_Log.csv'

# PID parameters
Kp = 1
Ki = 1
Kd = 1

# Temperature Setpoint [degC]
Setpoint = 35

LimitV = 6
LimitI = 3

# Sensors 
#Sensor_Address = '28-0316642118ff' 
Sensor_Address = '28-041663de08ff'

# SMU Reset
inst.write("reset()")

# SMU Configuration
inst.write("smua.source.func = smua.OUTPUT_DCAMPS")
inst.write("smua.source.leveli = 0")
inst.write("smua.source.limitv = 6")
inst.write("smua.measure.rangev = 6")
inst.write("smua.source.output = smua.OUTPUT_ON")

# Check file presence, write header
if (os.path.isfile(LogFile) == False):
	with open(LogFile, 'a') as EnvLog:
		EnvLog.write("TimeStamp,Set_Point,Temperature,Current,Voltage,Output\r\n")
		print ("File %s does not exist\r\n" % LogFile) 

LastError = 0
Timestamp = time.time() 
try:
	while True:
		with open(LogFile, 'a') as MeterLog:
				Sensor = open("/sys/bus/w1/devices/%s/w1_slave" %Sensor_Address)
				Readout = Sensor.read()
				Sensor.close()
				RawTemperature = Readout.split("\n")[1].split(" ")[9]
				Temperature = float(RawTemperature[2:])/1000
				# PID Part 
				Error=Setpoint-Temperature
				TimeDelta=time.time()-Timestamp 
				ErrorSum = (Error * TimeDelta)
				ErrorDelta= (Error - LastError) / TimeDelta
				Output = Kp * Error + Ki * ErrorSum + Kd * ErrorDelta
				LastError = Error
				Timestamp = time.time()  
				
				SMU_Current_Set =  Output/10
				# SMU Set/Read
				inst.write("smua.source.leveli = %f" %(SMU_Current_Set))
				inst.write("print(smua.measure.v())")
				SMU_Voltage = inst.read()
				inst.write("print(smua.measure.i())")
				SMU_Current = inst.read()

				# Print and Log Values
				print time.strftime("%d/%m/%Y\t%H:%M:%S") + ("\tSet Point: %.3f\tTemerature: %.3f\tSMU I Set: %.6f\tSMU V Readout: %.6f\tOutput: %.6f\r" % (float(Setpoint),float(Temperature),float(SMU_Current),float(SMU_Voltage),float(Output)))
				MeterLog.write (time.strftime("%d/%m/%Y-%H:%M:%S,") + ("%.3f,%.3f,%.6f,%.6f,%.6f\r" % (float(Setpoint),float(Temperature),float(SMU_Current),float(SMU_Voltage),float(Output))))
#		time.sleep(1)
except KeyboardInterrupt:
	inst.write("smua.source.output = smua.OUTPUT_OFF")
	MeterLog.close()




