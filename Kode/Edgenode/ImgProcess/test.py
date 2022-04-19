import cv2
import numpy as np

cap = cv2.VideoCapture(0) # Load webcam(0) or videofile with path to file.
while True: 
    ret, frame = cap.read() # ret tells if successful or not(true/false) and the readed image
    width = int(cap.get(3))
    height = int(cap.get(4))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)    # Convert BGR pixels into hue, saturation and lightness
    lower_color = np.array([90, 50, 50])            # Lower bound of color
    upper_color = np.array([130, 255, 255])         # Upper blond of color

    mask = cv2.inRange(hsv, lower_color, upper_color) # B/W image of the selected color spectrum

    result = cv2.bitwise_and(frame, frame, mask=mask) # adds color spectrum to B/W image

    cv2.imshow('window title', result)
    if cv2.waitKey(1) == ord('q'): # wait for 1 millisecond and awaits for a 'q' key press before closing the window
        break

cap.release()
cap.destroyAllWindows()