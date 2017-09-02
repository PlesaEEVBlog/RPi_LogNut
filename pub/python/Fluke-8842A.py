# Python script for testing the Fluke 8842A
# reads the voltage every second and prints it
import os.path
import sys
import Gpib
import time

# GPIB Address = 24
inst = Gpib.Gpib(0,24, timeout=60) 
inst.clear() 

# show instrument name and version
inst.write("G8")
print(inst.read())

# configure for VDC measurement
inst.write("F1")

# 20V range
inst.write("R3")

# slow rate
inst.write("S0")

# external trigger by GPIB command "?" for measurment
inst.write("T1")

while True:
    time.sleep(1)
    inst.write("?")
    volt = float(inst.read().strip())
    print("%f V" % (volt))
