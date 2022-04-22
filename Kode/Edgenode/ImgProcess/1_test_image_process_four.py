

#####################################################
# Display imported image in four different formats	#
# 	- Standard image								#
# 	- Greyscale image								#
#	- Blured image 									#
#	- Edged image									#
#													#
#####################################################


import cv2

# Load image, displays it and prints its dimensions.
path = '/home/wrongside/Documents/01 Comtek/01 Semester 4 project/git/ComTek4_Project/Kode/Edgenode/ImgProcess/test_drone.jpg' 	# Path to image
img = cv2.imread(path,-1) 																										# Reading the image using imread() function (-1 is default load, 0 is greyscale)
cv2.imshow('Drone', img) 																										# Display image


# Convert image to grey scale
grey = cv2.imread(path,0)
cv2.imshow('Grey', grey)


# Blur image - this will remove small noise in the image
blur = cv2.GaussianBlur(img, (7,7), cv2.BORDER_DEFAULT)
cv2.imshow('Blur', blur)


# Egde cascade - find all edges in image
edge = cv2.Canny(img,125,175)														# Number are thredshold
cv2.imshow('Edge', edge)


print(img.shape)		# print height, width and channels of image

# wait an infinite amount of time for you to press any key on the keyboard and then close the window
cv2.waitKey(0) 			 
cv2.destroyAllWindows()