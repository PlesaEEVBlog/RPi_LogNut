# Test RS232 over USB ( Keyspan USA-19hs serial adapter )
import serial
import time

ser = serial.Serial(
		port='/dev/ttyUSB0',
		baudrate = 19200,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=1
)

ser.write("*IDN?\n")
time.sleep(2)
bytesToRead = ser.inWaiting()
print ser.read(bytesToRead)

ser.close()
