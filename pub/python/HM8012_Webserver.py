#!/usr/bin/python

# simple example to show the current display of a HM8012 multimeter in a webpage

import BaseHTTPServer
import serial
import time

# bind address to access it from the everywhere
HOST_NAME = '0.0.0.0'
PORT_NUMBER = 8000

def command(cmd):
  ser.write(cmd + '\r')
  time.sleep(1)
  bytesToRead = ser.inWaiting()
  result = ser.read(bytesToRead)
  withoutControlCharacters = filter(lambda x: ord(x)>=32, result)
  return withoutControlCharacters
  
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
	  self.wfile.write('<html><head><title>HM8012 network measurement</title><meta http-equiv="refresh" content="1"></head>')
	  measure = command('S?')
	  self.wfile.write('<body><p style="font-family:courier;font-size:48pt;">' + measure + '</p>')
	  self.wfile.write('</body></html>')
	except KeyboardInterrupt:
	  httpd.server_close()

# open serial port
ser = serial.Serial(
		port='/dev/serial0',
		baudrate = 4800,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=1
)

# run webserver
server_class = BaseHTTPServer.HTTPServer
httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
try:
    httpd.serve_forever()
except:
    pass
httpd.server_close()
ser.close()
