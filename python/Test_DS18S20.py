#!/usr/bin/python2
import time
#Sensor_Address = '28-0316642118ff'  
Sensor_Address = '28-041663de08ff' 
try:
	while True:
		Sensor = open("/sys/bus/w1/devices/%s/w1_slave" %Sensor_Address)
		Readout = Sensor.read()
		Sensor.close()
		RawTemperature = Readout.split("\n")[1].split(" ")[9]
		Temperature = float(RawTemperature[2:])/1000
		print Temperature
		time.sleep(1)
except KeyboardInterrupt:
	pass

