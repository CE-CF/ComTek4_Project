import WiFi.WiFi
import ImgProcess.Img_process as analysis
import McC.McC as correction
import GUI.gui as Guisubmodule
import multiprocessing as mp
import socket, time, struct, math
import numpy as np
import cv2
import pickle


##############################################################
# Renaming
##############################################################

net = WiFi.WiFi # Just a renaming
manager = mp.Manager() # Multi processing manager. Used to create global variable.

##############################################################
# Variables
##############################################################

bufferSize = 65000 # Buffer size for receiving

##############################################################
# Variables: Shared memory
##############################################################

sharedFeed = manager.Value(bytes, 0xff) # Used to share the video feed between receive, gui and image processing task. 
detected = manager.Value(int, 0) # Used to evaluate of there is a drone detected. This can be 0 or 1
created = manager.Value(int, 0) # Used to manage if the Motor Correction calculation submodule has created a list of values. Can be 0 or 1

center1 = manager.Value(int, 0) # Used for storing center og image x-axis
center2 = manager.Value(int, 0) # Used for storing center of image y-axis
drone1 = manager.Value(int, 0) # Used for storing center of drone x-axis
drone2 = manager.Value(int, 0) # Used for storing center of drone y-axis

yawC = manager.Value(int, 0) # Used for storing the Yaw part of the packet
pitchC = manager.Value(int, 0) # Used for storing the pitch part of the packet

##############################################################
# Functions
##############################################################


def Receiverimg(BUFFER_SIZE):
    DAmount = 0 # Used as a checker for whether there has been a drone detected in 5 frames. D amount = Detection amount
    oldSequenceNum = 0 # Used for the receive function to check if it is an old image that has been received.
    while(1):
        try:
            image, oldSequenceNum = net.Receive(BUFFER_SIZE, oldSequenceNum) # Calling the receive function from the wifi submodule
            sharedFeed.set(image)                                           # Sharing the feed in global memory
            c1, c2, d1, d2 = analysis.drone_detection(sharedFeed.get()) # Calling the image processing submodule
            if d1 and d2 == 0:                                          # Checks if a there is a drone present
                drone1.set(d1)                                          # sets the drone coordinate to 0
                drone2.set(d2)                                          # sets the drone coordinate to 0
                DAmount = 0                                             # Detection amount is set to 0
                detected.set(0)                                         # If a drone is detected is set to false
            else:
                DAmount = DAmount + 1                                   # A drone is detected and the detection amount is added 1
            if DAmount > 4:
                center1.set(c2)            # Set center of frame x-axis.
                center2.set(c1)            # Set center of frame y-axis.
                drone1.set(d1)             # Set center of drone x-axis.
                drone2.set(d2)             # Set center of drone y-axis.
                detected.set(1)            # Set detection of drone to true
        except:
            print("Failed to receive...")  #Fail message

##############################
# Receive function
##############################

def Receiver(BUFFER_SIZE):
    oldSequenceNum = 0  # Used for the receive function to check if it is an old image that has been received.
    while(1):
        try:
            image, oldSequenceNum = net.Receive(BUFFER_SIZE, oldSequenceNum) # Use receive function from communication submodule
            sharedFeed.set(image)                                            # Sharing the feed in global memory
        except:
            print("Failed to receive...")                                    # Fail message
        


##############################
# Send function
##############################

def tcpSender():
    while(1):
        try:
            net.command_udp.connect(net.Sentry_ADDR)                        # Connect to Sentry unit via TCP
        except:
            pass    
        try:
            if detected.get() == 1 and yawC.get() != 0 and pitchC != 0:     # Checks if a drone is detected and coordinates are set.
                packet = struct.pack('bb', yawC.get(), pitchC.get())        # Packs the commands as two bytes.
                net.tcpSend(packet)                                         # Uses the communication module's TCPsend function.
        except:
            print("Failed to send...")                                      # Fail message
            pass

##############################
# Image Processing function
##############################

def imageProcessProcess():
    DAmount = 0   # Used as a checker for whether there has been a drone detected in 5 frames. D amount = Detection amount
    while(1):
        c1, c2, d1, d2 = analysis.drone_detection(sharedFeed.get()) # Calling the receive function from the wifi submodule
        if d1 and d2 == 0:                                          # Checks if a there is a drone present
            drone1.set(d1)                                          # sets the drone coordinate to 0
            drone2.set(d2)                                          # sets the drone coordinate to 0
            DAmount = 0                                             # Detection amount is set to 0
            detected.set(0)                                         # If a drone is detected is set to false
        else:
            DAmount = DAmount + 1                                   # A drone is detected and the detection amount is added 1
        if DAmount > 4:
            center1.set(c2)                                         # Set center of frame x-axis.
            center2.set(c1)                                         # Set center of frame y-axis.
            drone1.set(d1)                                          # Set center of drone x-axis.
            drone2.set(d2)                                          # Set center of drone y-axis.
            detected.set(1)                                         # If a drone is detected is set to true

##############################
# Motor Correction function
##############################

def McCorrection():
    correctionList = 0
    if detected.get() == 1 and drone1.get() != 0 and drone2.get() != 0:     # Checks if a drone is detected and coordinates are set.      
        imgList = [center1.get(), center2.get(), drone1.get(), drone2.get()]   # Sets the framesize and drone center in a list.
        yaw, pitch = correction.motorCorrection(imgList, 53, 4,correctionList,1,0)  # Call the motor correction submodule
        yawC.set(yaw)                                                               # Set yaw command to global memory
        pitchC.set(pitch)                                                           # Set pitch command to global memory
        with open("/home/madss/Documents/school/4S/projekt/ComTek4_Project/correctionList.pkl", 'rb') as f: # Open the lookup created
            correctionList = pickle.load(f)                                                                 # Set the lookup
        while(1):
            try:
                if detected.get() == 1 and drone1.get() != 0 and drone2.get() != 0: # Checks if a drone is detected, coordinates are set. 
                    imgList = [center1.get(), center2.get(), drone1.get(), drone2.get()] # Sets the framesize and drone center in a list.
                    yaw, pitch = correction.motorCorrection(imgList, 53, 4,correctionList,1,0) # Call the motor correction submodule
                    yawC.set(yaw)                                                              # Set yaw command to global memory
                    pitchC.set(pitch)                                                          # Set pitch command to global memory
            except:
                pass

##############################
# Gui function 
##############################

def Guiprocessfunction():
    time.sleep(2)                                                               # Just waits a bit
    while(1):
        try:
            Guisubmodule.gui(sharedFeed.get(), yawC.get(), pitchC.get())        # Runs the GUI submodule
        except:
            pass

##############################################################
# Main
##############################################################

if __name__ == '__main__':
    try:
        ##############################################################
        # Uncomment for program running in parallel
        ##############################################################
        sendProcess = mp.Process(target=tcpSender,)
        receiveProcess = mp.Process(target=Receiver, args=(bufferSize,))
        imgProcessor = mp.Process(target=imageProcessProcess,)
        McCProcess = mp.Process(target=McCorrection,)
        Guiprocess = mp.Process(target=Guiprocessfunction,)

        receiveProcess.start()
        imgProcessor.start()
        McCProcess.start()
        Guiprocess.start()
        sendProcess.start()

        receiveProcess.join()
        imgProcessor.join()
        McCProcess.join()
        Guiprocess.join()
        sendProcess.join()

        ##############################################################
        # Uncomment for receive and image processing sequentially
        ##############################################################
        # sendProcess = mp.Process(target=tcpSender,)
        # receiveimgProcess =mp.Process(target=Receiverimg, args=(bufferSize,))
        # McCProcess = mp.Process(target=McCorrection,)
        # Guiprocess = mp.Process(target=Guiprocessfunction,)

        # Start processes
        # receiveimgProcess.start()
        # McCProcess.start()
        # Guiprocess.start()
        # sendProcess.start()
        
        # Join Processes
        # receiveimgProcess.join()
        # McCProcess.join()
        # Guiprocess.join()
        # sendProcess.join()

    except KeyboardInterrupt:
        ##############################################################
        # Shutdown for parallel
        ##############################################################
        print("Shutting down....")
        net.closeDown()
        sendProcess.terminate()
        receiveProcess.terminate()
        imgProcessor.terminate()
        McCProcess.terminate()
        Guiprocess.terminate()
        print("Bye")

        ##############################################################
        # Shutdown for sequential
        ##############################################################
        # print("Shutting down....")
        # net.closeDown()
        # sendProcess.terminate()
        # McCProcess.terminate()
        # Guiprocess.terminate()
        # receiveimgProcess.terminate()
        # print("Bye")
