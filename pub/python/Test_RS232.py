# Test RS232  
import serial
import time

ser = serial.Serial(
		port='/dev/serial1',
		baudrate = 19200,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=1
)
print("Port " + ser.portstr + " opened : " + str(ser.isOpen()))

ser.write("*IDN?\n")
time.sleep(2)
bytesToRead = ser.inWaiting()
print ser.read(bytesToRead)

ser.close()
