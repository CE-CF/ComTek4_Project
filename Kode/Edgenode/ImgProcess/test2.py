import cv2
import numpy as np

def nothing(x):
    pass



    # Use a vido as source
#cap = cv2.VideoCapture(0); # when source is video

    # Set up trackbars for value adjustment
cv2.namedWindow("Tracking")
cv2.createTrackbar("LH", "Tracking", 0, 255, nothing)
cv2.createTrackbar("LS", "Tracking", 0, 255, nothing)
cv2.createTrackbar("LV", "Tracking", 0, 255, nothing)
cv2.createTrackbar("UH", "Tracking", 255, 255, nothing)
cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)

while True:
        # Use an image as source
    frame = cv2.imread('drone.jpg') # when source is image


    #_, frame = cap.read() # when source is video

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # convert BGR image to a HSV image
        # Hue is color
        # Saturation is the greyness
        # Value is the brightness
    
    cv2.namedWindow("HSV Editing")
    low_hue = cv2.getTrackbarPos("Low Hue", "HSV Editing")
    low_sat = cv2.getTrackbarPos("LS", "HSV Editing")
    low_v = cv2.getTrackbarPos("LV", "HSV Editing")

    u_h = cv2.getTrackbarPos("UH", "HSV Editing")
    u_s = cv2.getTrackbarPos("US", "HSV Editing")
    u_v = cv2.getTrackbarPos("UV", "HSV Editing")
    
    
    lower_bound_blue = np.array([l_h, l_s, l_v]) # 110,50,50
    upper_bound_blue = np.array([u_h, u_s, u_v]) # 130,255,255
    

    mask = cv2.inRange(hsv, lower_bound_blue, upper_bound_blue) # Threadshold image between lower and upper bound

    result = cv2.bitwise_and(frame, frame, mask=mask) # 'bit and' operation unites mask image with color image 

    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("res", result)

    if cv2.waitKey(1) == ord('q'):
        break


#cap.release() # when source is video
cv2.destroyAllWindows()


"""
low_red = np.array([161, 155, 84])
high_red = np.array([179, 255, 255])

low_green = np.array([25, 52, 72])
high_green = np.array([102, 255, 255])


low_blue = np.array([94, 80, 2])
high_blue = np.array([126, 255, 255])
"""