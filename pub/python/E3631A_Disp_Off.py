# Python Display-off for Agilent PSU
import sys
import Gpib
inst = Gpib.Gpib(0,5)
inst.clear()
inst.write("DISP OFF")