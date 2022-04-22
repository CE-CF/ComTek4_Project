#####################################################
#                                                   #
#####################################################

# Necessary libraries
import cv2
import numpy
import threading
from queue import Queue


# Video stream from webcam  
def drone_detection(q_h, q_w, q_x, q_y):
    cam = cv2.VideoCapture(0)
    kernel = numpy.ones((5 ,5), numpy.uint8)
    print("\n[STREAM] Video stream begins...")

    try:
        while True:
            ret, frame = cam.read()

            # Size of video frame
            height, width = frame.shape[:2]
            
            # Find center of frame and saves in global queue
            q_h.put(height/2)
            q_w.put(width/2)
            
            # Lower and upper bound of color [B, G, R]
            lower_color = numpy.array([110, 70, 70])      
            upper_color = numpy.array([130, 255, 255])

            # Convert frame to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Turn color range white and the rest black
            mask = cv2.inRange(hsv, lower_color, upper_color)
            
            # Reduce the noise on frame
            opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel) 
         
            # Extract coordinates, width and height of 
            x, y, w, h = cv2.boundingRect(opening)
         
            # Create rectangle and center dot
            cv2.rectangle(frame, (x, y), (x+w, y + h), (0, 255, 0), 3)
            cv2.circle(frame, (int(x+w/2), int(y+h/2)), 5, (0, 0, 255), -1)

            #  
            q_x.put(int(x+w/2))
            q_y.put(int(y+h/2))

            # Display video with rectangle and center dot
            cv2.imshow('Color detection', frame)

            # Press 'Esc' to exit window
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break
        print("[STREAM LOST] Video feed has been lost")
    except:
        pass

        

# Main program
if __name__ == "__main__":

    # Variables
    q_h = Queue()
    q_w = Queue()
    q_x = Queue()
    q_y = Queue()

    print("[START] Edge node starts...")
    video_feed = threading.Thread(target=drone_detection, args=(q_h, q_w, q_x, q_y))
    video_feed.start() 

    while True:
        height = q_h.get()
        width = q_w.get()
        
        x = q_x.get()
        y = q_y.get()
        print(f"Height:{height}\t Width:{width}\t X:{x}\t Y:{y}")   

    