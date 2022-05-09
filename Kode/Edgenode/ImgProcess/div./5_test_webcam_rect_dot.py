#####################################################
# Open webcam and display in a window.              #
#   - Program will look for a color range and put   #
#   a rectangle around it with a dot in the         #
#   middle.                                         #   
#                                                   #
#####################################################


import cv2
import numpy
 
cam = cv2.VideoCapture(0)
kernel = numpy.ones((5 ,5), numpy.uint8)
 
while (True):
    ret, frame = cam.read()

    # Lower and upper bound of color [B, G, R]
    lower_color = numpy.array([110, 70, 70])      
    upper_color = numpy.array([130, 255, 255])

    # Convert frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Turn color range white and the rest black
    mask = cv2.inRange(hsv, lower_color, upper_color)
    
    # Reduce the noise on frame
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel) 
 
    # Extract coordinates, width and height of 
    x, y, w, h = cv2.boundingRect(opening)
 
    # Create rectangle and center dot
    cv2.rectangle(frame, (x, y), (x+w, y + h), (0, 255, 0), 3)
    cv2.circle(frame, (int(x+w/2), int(y+h/2)), 5, (0, 0, 255), -1)

    # Display video with rectangle and center dot
    cv2.imshow('Color detection', frame)

    # Press 'Esc' to exit window
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break