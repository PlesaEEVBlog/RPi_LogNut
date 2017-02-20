#!/usr/bin/python2
# Test VXI11
import vxi11
instr = vxi11.Instrument("192.168.0.25")
print(instr.ask("*IDN?"))
