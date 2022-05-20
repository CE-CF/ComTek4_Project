#####################################################
#                                                   #
#####################################################

# Import libraries
import cv2
import numpy
import threading
import urllib.request
from math import floor

# cv2.namedWindow('Color detection', cv2.WINDOW_AUTOSIZE)

        
# Video stream from webcam  
def gui(feed, yaw, pitch):
    kernel = numpy.ones((5 ,5), numpy.uint8)
    #print("\n[STREAM] Video stream begins...")

    try:
        feed = numpy.fromstring(feed,numpy.uint8)
        frame = cv2.imdecode(feed, cv2.IMREAD_COLOR)
        # Size of video frame
        height, width = frame.shape[:2]
        # Find center of frame and saves in global queue
        q_h = int(height/2)
        q_w = int(width/2)
        
        # Lower and upper bound of color [B, G, R]
        lower_color = numpy.array([110, 70, 70])
        upper_color = numpy.array([130, 255, 255])

        # Convert frame to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Turn color range white and the rest black
        mask = cv2.inRange(hsv, lower_color, upper_color)

        # Reduce the noise on frame with kernel
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # Extract coordinates, width and height of 
        x, y, w, h = cv2.boundingRect(opening)

        # Create rectangle and center dot
        cv2.rectangle(frame, (x, y), (x+w, y + h), (0, 255, 0), 3)
        cv2.circle(frame, (int(x+w/2), int(y+h/2)), 5, (0, 0, 255), -1)

        #  
        q_x = int(x+w/2)
        q_y = int(y+h/2)
        
        # print("1")
        font = cv2.FONT_HERSHEY_SIMPLEX
        # print("2")
        if (yaw<0):
            yawText = f'Yaw:DEG: {-(abs(yaw)%32):3d} | SS {(floor(abs(yaw)/32)):1d}'
        else:
            yawText = f'Yaw:DEG: {(abs(yaw)%32):3d} | SS {(floor(abs(yaw)/32)):1d}'
        # print("3")
        if (pitch<0):
            pitchText = f'Pitch:DEG: {(abs(pitch)%32):3d} | SS {(floor(abs(pitch)/32)):1d}'
        else:
            pitchText = f'Pitch:DEG: {-(abs(pitch)%32):3d} | SS {(floor(abs(pitch)/32)):1d}'
        # print("mor")
        
        yaw1 = int(x+w/4)
        yaw2 = int(y+h+5) 
        pitch1 = int(x+(w/4)*3) 
        pitch2 = int(y+h+5)

        cv2.putText(frame, yawText,(10,50), font, 1, (0, 255, 255), 2, cv2.LINE_4)
        cv2.putText(frame, pitchText,(10,100), font, 1, (0, 255, 255), 2, cv2.LINE_4)
        # print("Din")

        cv2.imshow('Color detection', frame)
        key=cv2.waitKey(5)
        if key == ord('q'):
            return
        return
    except:
        # print("Img fejl")
        return 