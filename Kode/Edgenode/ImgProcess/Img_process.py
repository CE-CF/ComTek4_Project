#####################################################
#                                                   #
#####################################################

# Import libraries
import cv2
import numpy
import threading
import urllib.request

# Variables
url='http://192.168.1.238/cam-mid.jpg'


# Frame processing function  
def drone_detection(feed):

    kernel = numpy.ones((5 ,5), numpy.uint8)            # Noise reduction matrix(kernel)

    print("\n[STREAM] Video stream begins...")

    try:
        img_resp=urllib.request.urlopen(url)
        imgnp=numpy.array(bytearray(img_resp.read()),dtype=numpy.uint8)
        frame=cv2.imdecode(imgnp, -1)

        height, width = frame.shape[:2] # Get size of video frame
        
        # Lower and upper bound of color [B, G, R]
        lower_color = numpy.array([110, 70, 70])
        upper_color = numpy.array([130, 255, 255])

        # Convert frame to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        print("1") # Statement control

        # Turn color range white and the rest black
        mask = cv2.inRange(hsv, lower_color, upper_color)
        print("2") # Statement control

        # Calculate frame center
        frame_height_center = height/2
        frame_width_center = width/2
        print("3") # Statement control

        # Reduce the noise on frame with kernel
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        print("4") # Statement control

        # Extract coordinates, width and height of 
        x, y, w, h = cv2.boundingRect(opening)
        print("5") # Statement control

        # Calculate drone center
        drone_height_center = int(y+h/2)
        drone_width_center = int(x+w/2)
        print("6") # Statement control

        # Create rectangle and center dot
        cv2.rectangle(frame, (x, y), (x+w, y + h), (0, 255, 0), 3)
        cv2.circle(frame, (drone_width_center, drone_height_center), 5, (0, 0, 255), -1)
        print("7") # Statement control
        
        cv2.imshow('Color detection', frame) # Display video with rectangle and center dot

        # Press 'q' key on keyboard to terminate program
        key=cv2.waitKey(5)
        if key == ord('q'):
            return
        
        print("8") # Statement control 
        return(frame_height_center, frame_width_center, drone_width_center, drone_height_center)

    except:
        print("[ERROR] Frame processing")
        pass