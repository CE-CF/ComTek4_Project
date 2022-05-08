
# Intro to openCV library 

NOTE: 
The standard color module is RGB (red, green, blue).
OPENCV uses a BGR (blue, green, red) color module.

## Color bar
```
import numpy as np
import cv2

def nothing(x):
    print(x)

img = np.zeros((300,512,3), np.uint8)
cv2.namedWindow('image')

cv2.createTrackbar('B', 'image', 0, 255, nothing)
cv2.createTrackbar('G', 'image', 0, 255, nothing)
cv2.createTrackbar('R', 'image', 0, 255, nothing)

while True:
    cv2.imshow('image', img)
    if cv2.waitKey(1) == ord('q'):
        break

    b = cv2.getTrackbarPos('B', 'image')
    g = cv2.getTrackbarPos('G', 'image')
    r = cv2.getTrackbarPos('R', 'image')
    img[:] = [b, g, r]

cv2.destroyAllWindows()
```


## Read and display image in different modes
```
import cv2

# Load image, displays it and prints its dimensions.
path = '/home/wrongside/Documents/01 Comtek/01 Semester 4 project/git/drone.jpg' 	# Path to image
img = cv2.imread(path,-1) 															# Reading the image using imread() function (-1 is default load, 0 is greyscale)
cv2.imshow('Drone', img) 															# Display image


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

```


## Display laptop webcam or videofile.
```
import cv2

cap = cv2.VideoCapture(0) # Load webcam(0)
# cap = cv2.VidoCapture('path_to_vido_file', -1)

while True: 
	ret, frame = cap.read() # ret tells if successful or not(true/false) and the readed image
	cv2.imshow('window title', frame)
	if cv2.waitKey(1) == ord('q'): # wait for 1 millisecond and awaits for a 'q' key press before closing the window
		break

cap.release()
cap.destroyAllWindows()
```

## Color filter to webcam
```
import cv2
import numpy as np

cap = cv2.VideoCapture(0) # Load webcam(0) or videofile with path to file.
while True: 
	ret, frame = cap.read() # ret tells if successful or not(true/false) and the readed image
	width = int(cap.get(3))
	height = int(cap.get(4))

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 	# Convert BGR pixels into hue, saturation and lightness
	lower_color = np.array([90, 50, 50])			# Lower bound of color
	upper_color = np.array([130, 255, 255])			# Upper blond of color

	mask = cv2.inRange(hsv, lower_color, upper_color) # B/W image of the selected color spectrum

	result = cv2.bitwise_and(frame, frame, mask=mask) # adds color spectrum to B/W image

	cv2.imshow('window title', result)
	if cv2.waitKey(1) == ord('q'): # wait for 1 millisecond and awaits for a 'q' key press before closing the window
		break

cap.release()
cap.destroyAllWindows()
```

