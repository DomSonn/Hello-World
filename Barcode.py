'''
Script to use webcam or usb cam as a barcode scanner

Changing the ‘1’ in, “cap = cv2.VideoCapture(1)”, 
changes the camera used so if it doesn’t work with this try using 0 or 2 etc. 
depending on how many cameras are connected to the PC.

Payload of barcode is shown as an output
'''

import numpy as np
import cv2
import pyzbar.pyzbar as pyzbar
cap = cv2.VideoCapture(1)
while True:
    _, frame = cap.read()
    decodedObjects = pyzbar.decode(frame)
    for obj in decodedObjects:
        print("Data:", obj.data)
        points = obj.polygon
        if len(points) > 4:
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points;
        n = len(hull)
        for j in range(0, n):
            cv2.line(frame, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 115:
        break
