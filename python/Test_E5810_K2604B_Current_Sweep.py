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

# SMU Reset
inst.write("reset()")

# SMU Configuration
inst.write("smua.source.func = smua.OUTPUT_DCAMPS")
inst.write("smua.source.leveli = 0")
inst.write("smua.source.limitv = 6")
inst.write("smua.measure.rangev = 6")
inst.write("smua.source.output = smua.OUTPUT_ON")


try:
	while True:
		inst.write("smua.source.leveli = 0.5")
		inst.write("print(smua.measure.v())")
		data = inst.read()
		print time.strftime("%d/%m/%Y\t%H:%M:%S") + ("\tSMU Readout: %.6f\r" % (float(data)))
		time.sleep(1)
except KeyboardInterrupt:
	inst.write("smua.source.output = smua.OUTPUT_OFF")   




