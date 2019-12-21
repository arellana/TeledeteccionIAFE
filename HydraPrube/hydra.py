#!/usr/bin/env python

from threading import Thread
#import RPi.GPIO as GPIO
import serial
import time

def printIncoming(port):
	while True:
		rcv = port.readline()
		print(rcv)
try:
    port = serial.Serial("/dev/ttyUSB0", baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0, rtscts=0, timeout=3)
except:
    port = serial.Serial("/dev/ttyUSB1", baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0, rtscts=0, timeout=3)



""" port.write("000SN=?\r\n")
rcv = port.readline()
print(rcv)
#print(":".join("{:02x}".format(ord(c)) for c in rcv))
time.sleep(2)

port.write("000FV=?\r\n")
rcv = port.readline()
print(rcv)
#print(":".join("{:02x}".format(ord(c)) for c in rcv))
time.sleep(2)

port.write("000AD=?\r\n")
rcv = port.readline()
print(rcv)
#print(":".join("{:02x}".format(ord(c)) for c in rcv))
time.sleep(2)
 """
port.write("000PE=1\r\n")
rcv = port.readline()
print(rcv)
#print(":".join("{:02x}".format(ord(c)) for c in rcv))
time.sleep(5)

# thread = Thread(target = printIncoming, args = (port, ))
# thread.start()

while True:
	port.write("000TR\r\n")
	# rcv = port.readline()
	# print(rcv)
	#print(":".join("{:02x}".format(ord(c)) for c in rcv))
	time.sleep(5)

	port.write("000T0\r\n")

	rcv = port.readline()
	print(rcv)

 	# with open("hydra.dat", "a") as myfile:
	# 	myfile.write(rcv)


	#print(":".join("{:02x}".format(ord(c)) for c in rcv))
	time.sleep(2)

