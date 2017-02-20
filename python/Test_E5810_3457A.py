#!/usr/bin/python2
# Test Agilent E5810A
import vxi11
inst = vxi11.Instrument("192.168.0.27", "gpib0,22")
inst.write("END ALWAYS")
inst.write("ID?")
print(inst.read())

# Serial port is not working, needs check with Alex
#instr = vxi11.Instrument("192.168.0.27", "COM1:488")
#print(instr.ask("*IDN?")) 
