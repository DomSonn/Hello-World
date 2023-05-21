"""
Script to implement buttons for JCAM

JCAM is an RPi powered portable camera that uses the PiCamera.
The unit has buttons on the outside of a custom built housing
that turn the device on and off and start and stop the Image_Capture.py script.
There is also a neopixel ring on the front which can be turned on and off with 
another button.

"""

import RPi.GPIO as GPIO
import os
import board
import neopixel
import psutil
import subprocess
import signal
import time
from scipy.interpolate import interp1d

pixels = neopixel.NeoPixel(board.D18,16,brightness=0.1)
ls = (0,0,255)
pixels[0] = ls

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

a_pin = 27
b_pin = 17
m = interp1d([1,1024],[0.1,0.8])
# create discharge function for reading capacitor data
def discharge():
    GPIO.setup(a_pin, GPIO.IN)
    GPIO.setup(b_pin, GPIO.OUT)
    GPIO.output(b_pin, False)
    time.sleep(0.005)

# create time function for capturing analog count value
def charge_time():
    GPIO.setup(b_pin, GPIO.IN)
    GPIO.setup(a_pin, GPIO.OUT)
    count = 0
    GPIO.output(a_pin, True)
    while not GPIO.input(b_pin):
        count = count +1
    return count

# create analog read function for reading charging and discharging data
def analog_read():
    discharge()
    return charge_time()

def image_start(channel):
        os.system("python3 /home/pi/Image_Capture.py")
        
#GPIO.add_event_detect(23,GPIO.FALLING, callback=image_start, bouncetime=300)

try:
    run = 0
    run1 = 0
    run2 = 0
    while True:
        #neopixel.NeoPixel(board.D18,16,brightness=int(m(analog_read())))
        if GPIO.input(23)==0 and run ==0:
            rpistr = "python3 /home/pi/Image_Capture.py"
            ls = (0,255,0)
            pixels[0] = ls
            p = subprocess.Popen(rpistr, shell=True, preexec_fn=os.setsid)
            run = 1
            while GPIO.input(23)==0:
                time.sleep(0.1)
        if GPIO.input(23)==0 and run ==1:
            run = 0
            os.killpg(p.pid, signal.SIGTERM)
            pixels[0]=(0,0,255)
            ls = (0,0,255)
            while GPIO.input(23)==0:
                time.sleep(0.1)
                
        if GPIO.input(24)==0 and run1 ==0:
            pixels.fill((255,255,255))
            pixels[0] = ls
            run1 = 1
            while GPIO.input(24)==0:
                time.sleep(0.1)
        if GPIO.input(24)==0 and run1 ==1:
            run1 = 0
            pixels.fill((0,0,0))
            pixels[0]=ls
            while GPIO.input(24)==0:
                time.sleep(0.1)
                
        if GPIO.input(3)==0:
            pixels.fill((0,0,0))
            os.system("sudo shutdown -h now")
    
except KeyboardInterrupt:
    GPIO.cleanup()
    
GPIO.cleanup()
