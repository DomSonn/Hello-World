"""
Script to capture images using the PiCamera

pip install picamera

Use:
- Change the number in 'range' to how many photos you want to take
- Change the save directory in 'camera.capture' to the desired location
- Change the sleep time based on how quickly you want to take pictures
"""

from picamera import PiCamera
import time
camera = PiCamera()

for i in range(500):
    camera.capture('/code/Training-Data/JumboGreen{0:04d}.jpg'.format(i))
    time.sleep(0)
print('Taken')
