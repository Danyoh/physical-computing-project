#!/usr/bin/python
# Daniel Nguyen 201460890
# Thomas Hillson 190291950
import RPi.GPIO as GPIO
import time
import smbus
import time
import threading

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219

#Global Variables
ADDRESS = 0x48

GPIO.setmode(GPIO.BCM)

#Setting pins 18, 23, 24, 25 for input to the motor
GPIO.setup(18,GPIO.IN)
GPIO.setup(23,GPIO.IN)
GPIO.setup(24,GPIO.IN)
GPIO.setup(25,GPIO.IN)

#Stepper pins
stepper_pins=[18,23,24,25]

#Initialize max7219
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial)

GPIO.setup(stepper_pins,GPIO.OUT)

stepper_sequence=[]

#Infrared sensor address
AIN1 = 0x41

#Set up thermistor
BUS = smbus.SMBus(1)
AIN2 = 0x42
BUS.write_byte(ADDRESS,AIN2)
VALUE = BUS.read_byte(ADDRESS)

#full step
stepper_sequence.append([GPIO.HIGH, GPIO.LOW, GPIO.LOW,GPIO.LOW])
stepper_sequence.append([GPIO.LOW, GPIO.HIGH, GPIO.LOW,GPIO.LOW])
stepper_sequence.append([GPIO.LOW, GPIO.LOW, GPIO.HIGH,GPIO.LOW])
stepper_sequence.append([GPIO.LOW, GPIO.LOW, GPIO.LOW,GPIO.HIGH])

#half step
# stepper_sequence.append([GPIO.HIGH, GPIO.LOW, GPIO.LOW,GPIO.LOW])
# stepper_sequence.append([GPIO.HIGH, GPIO.HIGH, GPIO.LOW,GPIO.LOW])
# stepper_sequence.append([GPIO.LOW, GPIO.HIGH, GPIO.LOW,GPIO.LOW])
# stepper_sequence.append([GPIO.LOW, GPIO.HIGH, GPIO.HIGH,GPIO.LOW])
# stepper_sequence.append([GPIO.LOW, GPIO.LOW, GPIO.HIGH,GPIO.LOW])
# stepper_sequence.append([GPIO.LOW, GPIO.LOW, GPIO.HIGH,GPIO.HIGH])
# stepper_sequence.append([GPIO.LOW, GPIO.LOW, GPIO.LOW,GPIO.HIGH])
# stepper_sequence.append([GPIO.HIGH, GPIO.LOW, GPIO.LOW,GPIO.HIGH])

#full step or half step
numSteps = 512
#numSteps = 256

def maxRotation():

    while True:
        x = 0
        if (VALUE*3.3/255) > 1:
            for x in range(8):
                    with canvas(device) as draw:
                        draw.point((0,x), fill="white")
                        time.sleep(0.01)
                        draw.point((0,x-1), fill="white")
                        time.sleep(0.01)
                        draw.point((0,x-2), fill="white")
                        time.sleep(0.01)
                        draw.point((0,x-3), fill="white")
                        time.sleep(0.01)
                        draw.point((0,x-4), fill="white")
                        time.sleep(0.01)
                        draw.point((0,x-5), fill="white")
                        time.sleep(0.01)
                        draw.point((0,x-6), fill="white")
                        time.sleep(0.01)
                        draw.point((0,x-7), fill="white")
                        time.sleep(0.01)
        else:
                for x in reversed(range(8)):
                    with canvas(device) as draw:
                        draw.point((0,x), fill="white")
                        time.sleep(0.01)
                        draw.point((0,x+1), fill="white")
                        time.sleep(0.01)
                        draw.point((0,x+2), fill="white")
                        time.sleep(0.01)
                        draw.point((0,x+3), fill="white")
                        time.sleep(0.01)
                        draw.point((0,x+4), fill="white")
                        time.sleep(0.01)
                        draw.point((0,x+5), fill="white")
                        time.sleep(0.01)
                        draw.point((0,x+6), fill="white")
                        time.sleep(0.01)
                        draw.point((0,x+7), fill="white")
                        time.sleep(0.01)
    return

threadmax7219 = threading.Thread(name='maxRotation', target = maxRotation)
threadmax7219.start()

def stepMotor():
    BUS.write_byte(ADDRESS,AIN2)
    VALUE = BUS.read_byte(ADDRESS)
    BUS.write_byte(ADDRESS,AIN2)
    VALUE = BUS.read_byte(ADDRESS)
    BUS.write_byte(ADDRESS,AIN2)
    VALUE = BUS.read_byte(ADDRESS)
    BUS.write_byte(ADDRESS,AIN2)
    VALUE = BUS.read_byte(ADDRESS)
    BUS.write_byte(ADDRESS,AIN2)
    VALUE = BUS.read_byte(ADDRESS)
    print("AOUT Step Motor:%1.3f  " %(VALUE*3.3/255))
    time.sleep(0.1)
    return

def infraredSensor():
    BUS.write_byte(ADDRESS,AIN1)
    VALUE = BUS.read_byte(ADDRESS)
    BUS.write_byte(ADDRESS,AIN1)
    VALUE = BUS.read_byte(ADDRESS)

    print("AOUT Infrared Sensor:%1.3f  " %(VALUE*3.3/255), end = "\t")
    time.sleep(0.1)
    return
     

try:
    while (True):
        #AIN0 = 0x40 #Photoresistor, output voltage goes down when light level increases, range of (1.139 - 3.287)
        #AIN1 = 0x41 #infrared sensor
        #AIN2 = 0x42 #thermoresistor, output voltage goes up when temperature increases, range of (0 - 2.122)
        #AIN3 = 0x43 #potentiometer, changes linearly, range of (0 - 3.3), smallest change I can make is 0.013

        while True:
            infraredSensor()
            stepMotor()

            if (VALUE*3.3/255) > 1:
                for row in stepper_sequence:
                    GPIO.output(stepper_pins,row)
                    time.sleep(0.01)
            else:
                for row in reversed (stepper_sequence):
                    GPIO.output(stepper_pins,row)
                    time.sleep(0.01)

except KeyboardInterrupt:
	pass

GPIO.cleanup()