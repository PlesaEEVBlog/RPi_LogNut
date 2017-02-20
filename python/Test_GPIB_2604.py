#!/usr/bin/python2
# Test GPIB
import sys
import Gpib
instr = Gpib.Gpib(0,29)
instr.write("*IDN?")
print(instr.read())
