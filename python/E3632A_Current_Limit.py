#!/usr/bin/python2
# Python Display-off for Agilent PSU
import sys
import Gpib
import vxi11
import time

#inst = Gpib.Gpib(0,9,timeout=60)
inst = vxi11.Instrument("192.168.0.27", "gpib0,9")

inst.clear()
inst.write("*IDN?")
print(inst.read(100))
inst.write("*RST")
inst.write("*CLS")
inst.write("DISP ON")
inst.write("VOLTage:RANGe P15V") 

# TEC Module MAximum
inst.write("CURRent:PROTection 4.2")
inst.write("VOLTage:PROTection 15.45") 

# Change state of output relay on RS232 connector ( internal jumper indise PSU needs to mbe placed))
inst.write("OUTPut:RELay ON")


inst.write("VOLTage 15")
inst.write("CURRent 0.5")

inst.write("OUTput ON")
try:
  while True:
    inst.write("MEASure:VOLTage:DC?")
    Voltage =  inst.read(100)
    inst.write("MEASure:CURRent?")
    Current =  inst.read(100)
    print("Voltage : %.6f V\t Current: %.9f A" %(float(Voltage),float(Current)))

except KeyboardInterrupt:
  inst.write("OUTput OFF")
  #inst.write("DISP OFF")
