#!/usr/bin/python2
# Python Display-off for Agilent PSU
import sys
import Gpib
inst = Gpib.Gpib(0,5,timeout=60)
inst.clear()
inst.write("*IDN?")
print(inst.read(100))
inst.write("DISP OFF")