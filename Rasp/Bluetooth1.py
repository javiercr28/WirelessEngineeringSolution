#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-850 -*-

#Titulo				:Bluetooth1.py
#Descripción		:Comunicación Bluetooth.
#Autor          	:Javier Campos Rojas
#Fecha            	:Setiembre-2017
#Versión         	:1.0
#Notas          	:
#==============================================================================

import os
import glob
import time
import RPi.GPIO as GPIO
from bluetooth import *
from xbee import ZigBee
from xbee.thread import XBee
import serial

#os.system('modprobe w1-gpio')
#os.system('modprobe w1-term')

GPIO.setwarnings(False);
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)

#base_dir = '/sys/bus/w1/devices/'
#device_folder = glob.glob(base_dir + '28*')[0]
#device_file = device_folder + '/w1_slave'


PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

# Open serial port
ser = serial.Serial(PORT, BAUD_RATE)

# Create API object
#xbee = XBee(ser)
xbee = ZigBee(ser,escaped=True)

def read_temp():
    try:
        response = xbee.wait_read_frame()
        tempval=response['samples'][0]['adc-3']
        return tempval
    except KeyboardInterrupt:
        ser.close()

"""
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
       e time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c
"""
#while True:
#	print(read_temp())
#	time.sleep(1)


server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

#uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
uuid = "2f840c69-cecb-4b10-87e4-01b9d28c231c"

advertise_service( server_sock, "AquaPiServer",
	service_id = uuid,
	service_classes = [ uuid, SERIAL_PORT_CLASS ],
	profiles = [ SERIAL_PORT_PROFILE ],
	#protocols = [ OBEX_UUID ]
	)
while True:
	print "Waiting for connection on RFCOMM channel %d" % port
	client_sock, client_info = server_sock.accept()
	print "Accepted connection from ", client_info
	client_sock.send("Tempe")
	try:
		while True:
			data = client_sock.recv(1024)
			if len(data) == 0: break
			print "received [%s]" % data
			if data == 'temp':
				#data = 'Temperatura = '
				data = 'Temperatura = '+ str(read_temp())
			elif data == '111':
				GPIO.output(14,GPIO.HIGH)
				data = 'light on!'
			elif data == '000':
				GPIO.output(14,GPIO.LOW)
				data = 'light off!'
			elif data == 'out':
				GPIO.output(14,GPIO.LOW)
				client_sock.close()
				break
			else:
				data = 'WTF!'
			client_sock.send(data)
			print "sending [%s]" % data
	except IOError:
		break
		
	except KeyboardInterrupt:
		print "disconnected"
		client_sock.close()
		server_sock.close()
		print "all done"
		break
