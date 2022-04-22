
#####################################################
# Show imported image in four different formats	    #
# 	- Standard image								#
# 	- HSV image										#
#	- Blured image 									#
#	- Edged image									#
#													#
#####################################################


# Load an image and looks for a certain range of blue


import cv2
import numpy
 

# Read image
path = '/home/wrongside/Documents/01 Comtek/01 Semester 4 project/git/ComTek4_Project/Kode/Edgenode/ImgProcess/blue_drone.jpg'  # Path to image
frame = cv2.imread(path,1)

# Convert frame to HSV
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Lower and upper bound of color [B, G, R]
lower_color = np.array([110, 70, 70])            
upper_color = np.array([130, 255, 255]) 


mask = cv2.inRange(hsv, lower_color, upper_color) # B/W image of the selected color spectrum

gray = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)

result = cv2.bitwise_and(frame, frame, mask=mask) # adds color spectrum to B/W image

cv2.imshow('Original', frame)
cv2.imshow('HSV', hsv)
cv2.imshow('Mask', mask)
cv2.imshow('Final state', result)
#cv2.imshow('Grey', gray)



cv2.waitKey(0)           
cv2.destroyAllWindows()
