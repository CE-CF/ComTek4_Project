import cv2
import numpy

kernel = numpy.ones((5 ,5), numpy.uint8)

# Read image
path = '/home/wrongside/Documents/01 Comtek/01 Semester 4 project/Github/ComTek4_Project/Kode/Edgenode/ImgProcess/blue_drone.png'  # Path to image
frame = cv2.imread(path,1)

# Convert frame to HSV
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Lower and upper bound of color [B, G, R]
lower_color = numpy.array([110, 70, 70])            
upper_color = numpy.array([130, 255, 255]) 

# Turn color range white and the rest black
mask = cv2.inRange(hsv, lower_color, upper_color) # B/W image of the selected color spectrum

opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel) 

# White pixels in mask will be given their orginal colors back.
result = cv2.bitwise_and(frame, frame, mask=mask) # adds color spectrum to B/W image

# Show the four images 
cv2.imshow('Original', frame)
cv2.imshow('HSV', hsv)
cv2.imshow('Mask', mask)
cv2.imshow('Opening', opening)

#cv2.imshow('Final state', result)

cv2.waitKey(0)           
cv2.destroyAllWindows()