# Following part is test GPIB  connection
import Gpib
import sys
instr =  Gpib.Gpib(0,28)
instr.write("*IDN?")
print(instr.read())

