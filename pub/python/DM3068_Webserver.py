#!/usr/bin/python

# Simple example to show the current display of a Rigol DM3068 MultiMeter in a webpage.

import BaseHTTPServer
import vxi11
import usbtmc
import serial
import Gpib
import time

# bind address to access it from the everywhere
HOST_NAME = '0.0.0.0'
PORT_NUMBER = 8000

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def do_GET(self):
	try:
	  self.send_response(200)
	  self.send_header('Content-type', 'text/html')
	  self.end_headers()
	  self.wfile.write('<html><head><title>Rigol DM3068 Multi Meter Network Measurement</title><meta http-equiv="refresh" content="1"></head>')
	  measurevalue = str(float(inst.ask(":MEASure:VOLTage:DC?")))
	  self.wfile.write('<body><p style="font-family:courier;font-size:48pt;">' + measurevalue + ' Volts </p>')
	  self.wfile.write('</body></html>')
	except KeyboardInterrupt:
	  httpd.server_close()

# Rigol DM3068 Multi Meter Device LAN Connectivity
inst = vxi11.Instrument("192.168.1.201")
inst.clear()

# Rigol DM3068 Multi Meter Device USB Connectivity
#inst = usbtmc.Instrument("USB::0x1ab1::0x0c94::INSTR")
#inst.clear()

# Rigol DM3068 GPIB Connection
# inst = Gpib.Gpib(0,7)
# inst.clear()

# Rigol DM3068 Multi Meter Device Serial Connectivity
# ser = serial.Serial(
#		port='/dev/serial1',
#		baudrate = 19200,
#		parity=serial.PARITY_NONE,
#		stopbits=serial.STOPBITS_ONE,
#		bytesize=serial.EIGHTBITS,
#		timeout=1
# )
# print("Port " + ser.portstr + " opened : " + str(ser.isOpen()))
# ser.write("*IDN?\n")
#
# time.sleep(2)
# bytesToRead = ser.inWaiting()
# print ser.read(bytesToRead)
#
# ser.close()

inst.write("*CLS")
inst.write("SYSTem:DISPlay:BRIGht 32")
inst.write("[SENSe:]ZERO:AUTO OFF")
inst.write('DISPlay:TEXT "Web Server View"')
inst.write("SYSTem:BEEPer:STATe ON")
inst.write("SYSTem:BEEPer")
inst.write("SYSTem:BEEPer:STATe OFF")
inst.write(":FUNCtion:VOLTage:DC")
inst.write("CONFigure:VOLTage:DC 20 V")

# run webserver
server_class = BaseHTTPServer.HTTPServer
httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
try:
    httpd.serve_forever()
except:
    pass
httpd.server_close()
inst.close()
