# Test GPIB
import sys
import Gpib
instr = Gpib.Gpib(0,16)
instr.write("*IDN?")
print(instr.read())
