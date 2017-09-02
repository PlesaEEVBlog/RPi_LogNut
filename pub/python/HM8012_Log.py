#!/usr/bin/python

# HM8012 log test
# for a list of available commands, see here:
# https://cdn.rohde-schwarz.com/pws/dl_downloads/dl_common_library/dl_manuals/gb_1/h/hm8012_1/HM8012_Digit_Multimeter_UserManual_de_en_03.pdf
# interactive test: sudo minicom -D /dev/serial0 -b 4800

import serial
import time
import sys

# open serial port
ser = serial.Serial(
		port='/dev/serial0',
		baudrate = 4800,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=1
)
print("Port " + ser.portstr + " opened : " + str(ser.isOpen()))

def command(cmd):
  ser.write(cmd + '\r')
  time.sleep(1)
  bytesToRead = ser.inWaiting()
  result = ser.read(bytesToRead)
  withoutControlCharacters = filter(lambda x: ord(x)>=32, result)
  return withoutControlCharacters
  
# test device identification
identification = command('I?')
print('identification: ' + identification)
if 'HM8012' not in identification:
  print('no HM8012 device found')
  ser.close()
  sys.exit(1)

# measure volts
command("VO")

# measure DC
command("DC")

# write log file, measure every 10 seconds
LogDir = '/pub/logs/'
LogFile= LogDir + 'HM8012_Log.csv'

starttime = time.time() - 9
with open(LogFile, 'w') as MeterLog:
  MeterLog.write('TimeStamp,Voltage\n')
while True:
  time.sleep(10.0 - ((time.time() - starttime) % 10.0))
  # file is closed while waiting, so that it can be loaded from the webserver
  with open(LogFile, 'a') as MeterLog:
    timestamp = time.strftime("%d/%m/%Y-%H:%M:%S")
    volt = command("S?").split()[0]
    line = timestamp + ',' + volt
    MeterLog.write(line + '\n')
    print(line)

ser.close()
