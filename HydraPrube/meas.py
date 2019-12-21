#!/usr/bin/env python2

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import serial
import time
import sys
from time import sleep
from datetime import datetime

LED_PIN = 12
SHUTDOWN_SECONDS = 5

########################################################
def button_callback(channel):
	sleep(.5)
	start = time.time()
	duration = 0
	while GPIO.input(10) == GPIO.HIGH and duration < SHUTDOWN_SECONDS :
		duration = time.time() - start

	if duration < SHUTDOWN_SECONDS :
		blinkLedTimes(2)
		print("Button was pushed!")
		port.write("000TR\r\n")
		time.sleep(5)

		port.flushInput()
		port.write("000T0\r\n")
		rcv = port.readline()
		blinkLedTimes(5)
		
		now = datetime.now() # current date and time
		date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
		with open("/home/pi/output.txt", "a") as out:
			out.write(date_time + " " + rcv)

		print(rcv)
		print(":".join("{:02x}".format(ord(c)) for c in rcv))
	else :
		exit()
		sys.exit(0)

########################################################
def exit() :
	GPIO.output(LED_PIN, GPIO.HIGH)
	sleep(5)
	GPIO.output(LED_PIN, GPIO.LOW)
	GPIO.cleanup() # Clean up
	port.close()
	shutdown()
	sys.exit(0)

########################################################
def blinkLedTimes(c):
	for i in range(c):
		GPIO.output(LED_PIN, GPIO.HIGH)
		sleep(.25)
		GPIO.output(LED_PIN, GPIO.LOW)
		sleep(.25)

########################################################
def shutdown():
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output

port = serial.Serial("/dev/ttyUSB0", baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0, rtscts=0, timeout=3)

port.write("000PE=1\r\n")
rcv = port.readline()
print(rcv)
#print(":".join("{:02x}".format(ord(c)) for c in rcv))
time.sleep(5)

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
# GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback, bouncetime=200) # Setup event on pin 10 rising edge
GPIO.setup(LED_PIN, GPIO.OUT)

ledFlag = False

blinkLedTimes(3)

# message = raw_input("Press enter to quit\n\n") # Run until someone presses enter
while True :
	if GPIO.input(10) == GPIO.HIGH :
		button_callback(10)

