#####################################################
#                                                   #
#####################################################

# Necessary libraries
import cv2
import numpy
import threading
import time



# Video stream from webcam 
def drone_detection():
    cam = cv2.VideoCapture(0)
    kernel = numpy.ones((5 ,5), numpy.uint8)
    print("\n[STREAM] Video stream begins...")

    measure_time = 0
    frames = 0
    try:        
        while True:
                
            t_start = time.time()
            ret, frame = cam.read()

            # Size of video frame
            height, width = frame.shape[:2]
            
            # Lower and upper bound of color [B, G, R]
            lower_color = numpy.array([110, 70, 70])
            upper_color = numpy.array([130, 255, 255])

            # Convert frame to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Turn color range white and the rest black
            mask = cv2.inRange(hsv, lower_color, upper_color)


            # Find center of frame and saves in global queue
            q_h = height/2
            q_w = width/2

            # Reduce the noise on frame
            opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

            # Extract coordinates, width and height of 
            x, y, w, h = cv2.boundingRect(opening)

            q_x = int(x+w/2)
            q_y = int(y+h/2)

            # Create rectangle and center dot
            cv2.rectangle(frame, (x, y), (x+w, y + h), (0, 255, 0), 3)
            cv2.circle(frame, (q_x, q_y), 5, (0, 0, 255), -1)
            
            
            # Display video with rectangle and center dot
            #cv2.imshow('HSV', hsv)
            #cv2.imshow('Mask', mask)
            #cv2.imshow('Noise reduction', opening)
            #cv2.imshow('Detection', frame)
            
            #print(f"Frame center: {int(width/2)},{int(height/2)}\t Drone center: {x},{y}")   


            key=cv2.waitKey(5)
            if key == ord('q'):
                return
            t_end = time.time()
            

            measure_time += t_end-t_start
            

            #if frames == 100:
               #print(measure_time/100)
            frames += 1
            if frames == 1000:
                print(f"Average time for 1000 frames: {measure_time/1000}")
            #print(frames)

    except:
        print("Papas mor")
        pass

if __name__ == "__main__":

    drone_detection()

