#####################################################
# 
#													#
#####################################################
   
import cv2
   
# path
path = '/home/wrongside/Documents/01 Comtek/01 Semester 4 project/Github/ComTek4_Project/Kode/Edgenode/ImgProcess/drone4.png' 	# Path to image

# Reading an image in default mode
image = cv2.imread(path,-1)
  
# Center coordinates
center_coordinates = (65, 220)
 
# Radius of circle
radius = 30
  
# Red color in BGR
color = (250, 0, 0)
  
# Line thickness of -1 px
thickness = -1
  
# Draw a circle of red color of thickness -1 px
image = cv2.circle(image, center_coordinates, radius, color, thickness)
  
# Displaying the image
cv2.imshow('window_name', image)
cv2.waitKey(0)
cv2.destroyAllWindows()