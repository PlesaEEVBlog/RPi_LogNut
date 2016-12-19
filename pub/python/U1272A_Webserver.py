#!/usr/bin/python

# Simple example to show the current display of a Rigol DM3068 MultiMeter in a webpage

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
	  measurevalue = str(float(send_receive('FETC?')))
	  self.wfile.write('<body><p style="font-family:courier;font-size:48pt;">' + measurevalue + ' Volts </p>')
	  self.wfile.write('</body></html>')
	except KeyboardInterrupt:
	  httpd.server_close()

# Rigol DM3068 Multi Meter Device LAN Connectivity
ser = serial.Serial(
		port='/dev/ttyUSB0',
		baudrate = 19200,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=0.5
)

def send_receive(command):
    ser.write(command + '\n')
    time.sleep(0.02)
    received = ser.read(100)
    received = received.replace('\n','')
    return received

# Setup the Keysight U1272A Meter
send_receive('*RST')
send_receive('CONF:VOLT:DC')
send_receive('*IDN?')
time.sleep(0.1)


# run webserver
server_class = BaseHTTPServer.HTTPServer
httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
try:
    httpd.serve_forever()
except:
    pass
httpd.server_close()
ser.close()
