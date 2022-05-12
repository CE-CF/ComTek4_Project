
import cv2
import numpy

# Read image
path = '/home/wrongside/Documents/01 Comtek/01 Semester 4 project/Github/ComTek4_Project/Kode/Edgenode/ImgProcess/blue_drone.png'  # Path to image
frame = cv2.imread(path,1)



# Size of video frame
height, width = frame.shape[:2]

# Find center of frame and saves in global queue
#q_h.put(height/2)
#q_w.put(width/2)

# Lower and upper bound of color [B, G, R]
lower_color = numpy.array([110, 70, 70])      
upper_color = numpy.array([130, 255, 255])

# Convert frame to HSV
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Turn color range white and the rest black
mask = cv2.inRange(hsv, lower_color, upper_color)

# Reduce the noise on frame
#opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel) 

# Extract coordinates, width and height of 
x, y, w, h = cv2.boundingRect(mask)

# Create rectangle and center dot
cv2.rectangle(frame, (x, y), (x+w, y + h), (0, 255, 0), 3)
cv2.circle(frame, (int(x+w/2), int(y+h/2)), 5, (0, 0, 255), -1)

#  
#q_x.put(int(x+w/2))
#q_y.put(int(y+h/2))

# Display video with rectangle and center dot
cv2.imshow('Color detection', frame)
cv2.waitKey(0)           
cv2.destroyAllWindows()