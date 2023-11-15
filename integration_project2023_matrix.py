#!/usr/bin/python
# Integration/Exploration Project CP320 Fall 2023
# Daniel Nguyen 201460890
# Thomas Hillson 190291950

#Importing Libraries
import RPi.GPIO as GPIO
import time
import smbus
import threading

#Library for max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219

#Setting up GPIO mode
GPIO.setmode(GPIO.BCM)
MOTOR_DIRECTION = "Counterclockwise"

#Setting pins 18, 23, 24, 25 for input to the motor
GPIO.setup(18,GPIO.IN)
GPIO.setup(23,GPIO.IN)
GPIO.setup(24,GPIO.IN)
GPIO.setup(25,GPIO.IN)
STEPPER_PINS=[18,23,24,25]
GPIO.setup(STEPPER_PINS,GPIO.OUT)
STEPPER_SEQUENCE = []
STEPPER_SEQUENCE.append([GPIO.HIGH, GPIO.LOW, GPIO.LOW,GPIO.LOW])
STEPPER_SEQUENCE.append([GPIO.LOW, GPIO.HIGH, GPIO.LOW,GPIO.LOW])
STEPPER_SEQUENCE.append([GPIO.LOW, GPIO.LOW, GPIO.HIGH,GPIO.LOW])
STEPPER_SEQUENCE.append([GPIO.LOW, GPIO.LOW, GPIO.LOW,GPIO.HIGH])

#Initialize max7219
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial)

#Setting up YL_40 (PCF8591 module) addresses and variables
ADDRESS = 0x48
BUS = smbus.SMBus(1)
AIN1 = 0x41 #Infrared sensor
AIN2 = 0x42 #Thermistor
BUS.write_byte(ADDRESS,AIN1)
VALUE_IR = BUS.read_byte(ADDRESS)
VALUE_MOTOR = VALUE_IR


#Convert value for A/D
def convertValue(value):
    voltage = 3.3
    max_bits = 255
    return value*voltage/max_bits

#Max7219 
def maxMatrix():
    max_matrix_sleep_seconds = 0.01
    max_matrix_start_position = 0

    while True:
                #IR display
        BUS.write_byte(ADDRESS,AIN1)
        VALUE_IR = BUS.read_byte(ADDRESS)
        BUS.write_byte(ADDRESS,AIN1)
        VALUE_IR = BUS.read_byte(ADDRESS)
        if (convertValue(VALUE_IR) > 3.2):
            with canvas(device) as draw:
                for x_position in range(7,0,-1):
                    draw.point((x_position,7), fill = "white")
                    draw.point((x_position,6), fill = "white")
                    draw.point((x_position,5), fill = "white")
                    draw.point((x_position,4), fill = "white")
                    draw.point((x_position,3), fill = "white")
                    draw.point((x_position,2), fill = "white")
                    draw.point((x_position,1), fill = "white")
                    draw.point((x_position,0), fill = "white")
        elif (convertValue(VALUE_IR) > 3.1):
            with canvas(device) as draw:
                for x_position in range(7,2,-1):
                    draw.point((x_position,7), fill = "white")
                    draw.point((x_position,6), fill = "white")
                    draw.point((x_position,5), fill = "white")
                    draw.point((x_position,4), fill = "white")
                    draw.point((x_position,3), fill = "white")
                    draw.point((x_position,2), fill = "white")
                    draw.point((x_position,1), fill = "white")
                    draw.point((x_position,0), fill = "white")
        elif (convertValue(VALUE_IR) > 3.05):
            with canvas(device) as draw:
                for x_position in range(7,4,-1):
                    draw.point((x_position,7), fill = "white")
                    draw.point((x_position,6), fill = "white")
                    draw.point((x_position,5), fill = "white")
                    draw.point((x_position,4), fill = "white")
                    draw.point((x_position,3), fill = "white")
                    draw.point((x_position,2), fill = "white")
                    draw.point((x_position,1), fill = "white")
                    draw.point((x_position,0), fill = "white")
        else:
            for x_position in range(7,6,-1):
                with canvas(device) as draw:
                    draw.point((x_position,7), fill = "white")
                    draw.point((x_position,6), fill = "white")
                    draw.point((x_position,5), fill = "white")
                    draw.point((x_position,4), fill = "white")
                    draw.point((x_position,3), fill = "white")
                    draw.point((x_position,2), fill = "white")
                    draw.point((x_position,1), fill = "white")
                    draw.point((x_position,0), fill = "white")
                    
        
        #Getting proper motor value
        BUS.write_byte(ADDRESS,AIN2)
        VALUE_MOTOR = BUS.read_byte(ADDRESS)
        BUS.write_byte(ADDRESS,AIN2)
        VALUE_MOTOR = BUS.read_byte(ADDRESS)
        BUS.write_byte(ADDRESS,AIN2)
        VALUE_MOTOR = BUS.read_byte(ADDRESS)
        BUS.write_byte(ADDRESS,AIN2)
        VALUE_MOTOR = BUS.read_byte(ADDRESS)
        BUS.write_byte(ADDRESS,AIN2)
        VALUE_MOTOR = BUS.read_byte(ADDRESS)

        #Motor value matrix display
        if (convertValue(VALUE_MOTOR)) > 0.5:
            for trailing_count in range(8):
                    with canvas(device) as draw:
                        draw.point((max_matrix_start_position,trailing_count), fill="white")
                        time.sleep(max_matrix_sleep_seconds)
                        draw.point((max_matrix_start_position,trailing_count-1), fill="white")
                        time.sleep(max_matrix_sleep_seconds)
                        draw.point((max_matrix_start_position,trailing_count-2), fill="white")
                        time.sleep(max_matrix_sleep_seconds)
                        draw.point((max_matrix_start_position,trailing_count-3), fill="white")
                        time.sleep(max_matrix_sleep_seconds)
                        draw.point((max_matrix_start_position,trailing_count-4), fill="white")
                        time.sleep(max_matrix_sleep_seconds)
                        draw.point((max_matrix_start_position,trailing_count-5), fill="white")
                        time.sleep(max_matrix_sleep_seconds)
                        draw.point((max_matrix_start_position,trailing_count-6), fill="white")
                        time.sleep(max_matrix_sleep_seconds)
                        draw.point((max_matrix_start_position,trailing_count-7), fill="white")
                        time.sleep(max_matrix_sleep_seconds)
        else:
                for trailing_count in reversed(range(8)):
                    with canvas(device) as draw:
                        draw.point((max_matrix_start_position,trailing_count), fill="white")
                        time.sleep(max_matrix_sleep_seconds)
                        draw.point((max_matrix_start_position,trailing_count+1), fill="white")
                        time.sleep(max_matrix_sleep_seconds)
                        draw.point((max_matrix_start_position,trailing_count+2), fill="white")
                        time.sleep(max_matrix_sleep_seconds)
                        draw.point((max_matrix_start_position,trailing_count+3), fill="white")
                        time.sleep(max_matrix_sleep_seconds)
                        draw.point((max_matrix_start_position,trailing_count+4), fill="white")
                        time.sleep(max_matrix_sleep_seconds)
                        draw.point((max_matrix_start_position,trailing_count+5), fill="white")
                        time.sleep(max_matrix_sleep_seconds)
                        draw.point((max_matrix_start_position,trailing_count+6), fill="white")
                        time.sleep(max_matrix_sleep_seconds)
                        draw.point((max_matrix_start_position,trailing_count+7), fill="white")
                        time.sleep(max_matrix_sleep_seconds)      
        
    return

#Max7219 Segment
def maxSegment():
     
    max_segment_sleep_seconds = 0.01

    x_components =  [7,7,7,6,5,4,3,2,1,0,0,0,0,1,2,3,4,5,6,7]
    y_components = [2,1,6,6,6,6,6,6,6,6,5,4,3,3,3,3,3,3,3,3]

    while True:
        BUS.write_byte(ADDRESS,AIN1)
        VALUE_IR = BUS.read_byte(ADDRESS)
        BUS.write_byte(ADDRESS,AIN1)
        VALUE_IR = BUS.read_byte(ADDRESS)
        if (convertValue(VALUE_IR) > 3.1):
            max_segment_sleep_seconds = 0.001
        else:
            max_segment_sleep_seconds = 0.1

        for led_position in range(len(x_components)):
            with canvas(device) as draw:
                draw.point((x_components[led_position],y_components[led_position]), fill="white")
                time.sleep(max_segment_sleep_seconds)


#Output for stepper motor
#Bus write/read multiple times to clear previous values
def stepMotorOutput():
    stepper_sleep_seconds = 0.01

    BUS.write_byte(ADDRESS,AIN2)
    VALUE_MOTOR = BUS.read_byte(ADDRESS)
    BUS.write_byte(ADDRESS,AIN2)
    VALUE_MOTOR = BUS.read_byte(ADDRESS)
    BUS.write_byte(ADDRESS,AIN2)
    VALUE_MOTOR = BUS.read_byte(ADDRESS)
    BUS.write_byte(ADDRESS,AIN2)
    VALUE_MOTOR = BUS.read_byte(ADDRESS)
    BUS.write_byte(ADDRESS,AIN2)
    VALUE_MOTOR = BUS.read_byte(ADDRESS)

    if (convertValue(VALUE_MOTOR)) > 0.5:
        MOTOR_DIRECTION = "Clockwise"
        for row in STEPPER_SEQUENCE:
            GPIO.output(STEPPER_PINS,row)
            time.sleep(stepper_sleep_seconds)
    else:
        MOTOR_DIRECTION = "Counterclockwise"
        for row in reversed (STEPPER_SEQUENCE):
            GPIO.output(STEPPER_PINS,row)
            time.sleep(stepper_sleep_seconds)


    print("AOUT Step Motor:%1.3f" %(convertValue(VALUE_MOTOR)), "\t" , MOTOR_DIRECTION)
    time.sleep(0.1)

    
    return

#Output for infrared sensor
#Bus write/read mutliple times to clear previous values
def infraredSensorOutput():
    BUS.write_byte(ADDRESS,AIN1)
    VALUE_IR = BUS.read_byte(ADDRESS)
    BUS.write_byte(ADDRESS,AIN1)
    VALUE_IR = BUS.read_byte(ADDRESS)

    print("AOUT Infrared Sensor:%1.3f" %(convertValue(VALUE_IR)), end = "\t")
    time.sleep(0.1)
    return

threadMaxMatrix = threading.Thread(name='maxMatrix', target = maxMatrix)
threadMaxMatrix.start()

# threadMaxSegment = threading.Thread(name='maxSegment', target = maxSegment)
# threadMaxSegment.start()

def main():

    try:
        while True:
            infraredSensorOutput()
            stepMotorOutput()
            


    except KeyboardInterrupt:
        pass

    GPIO.cleanup()

#Start main function

main()
     
     