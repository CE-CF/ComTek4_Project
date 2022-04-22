
#####################################################
# Open webcam and display in a window.              #
#   - The window will only show colors within the   #
#   limit range. Rest of the window will be black.  #
#                                                   #
#####################################################

import cv2
import numpy as np

cap = cv2.VideoCapture(0) # Load webcam(0) or videofile with path to file.

while True: 
    ret, frame = cap.read() 

    # Convert frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Lower and upper bound of color [B, G, R]
    lower_color = np.array([110, 70, 70])            
    upper_color = np.array([130, 255, 255])         

    # Turn color range white and the rest black
    mask = cv2.inRange(hsv, lower_color, upper_color) 

    # White pixels in mask will be given their orginal colors back.
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Show video feed from webcam
    cv2.imshow('window title', result)
    
    # Press 'q' to close video feed from webcam
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cap.destroyAllWindows()