import cv2

# Image path
path_img = 'on figure \ref{fig: implement_image_blue}.  '

# Read image
img = cv2.imread(path_img, cv2.IMREAD_UNCHANGED)

# Print original dimensions
print('Original Dimensions : ',img.shape)

# Downscale calculations
scale_percent = 30 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
  
# resize image
resized = cv2.resize(img, dim)
# Print resize image dimensions
print('Resized Dimensions : ',resized.shape)
 
# Filename
filename = 'drone3.jpg'
  
# Saving the image
cv2.imwrite(filename, img)


cv2.imshow("Resized image", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()