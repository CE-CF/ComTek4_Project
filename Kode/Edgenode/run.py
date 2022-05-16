import WiFi.WiFi
import ImgProcess.Img_process as analysis
import McC.McC as correction
import multiprocessing as mp
import socket, time, struct, math
import numpy as np
import cv2
import pickle

##############################################################
# Renaming
##############################################################

net = WiFi.WiFi
manager = mp.Manager()

##############################################################
# Variables
##############################################################

bufferSize = 65000

##############################################################
# Variables: Shared memory
##############################################################

sharedFeed = manager.Value(bytes, 0xff)
detected = manager.Value(int, 0)
created = manager.Value(int, 0)

center1 = manager.Value(int, 0)
center2 = manager.Value(int, 0)
drone1 = manager.Value(int, 0)
drone2 = manager.Value(int, 0)

yawC = manager.Value(int, 0)
pitchC = manager.Value(int, 0)

##############################################################
# Functions
##############################################################

##############################
# Receive function
##############################

def Receiver(BUFFER_SIZE):
    while(1):
        try:
            image = net.Receive(BUFFER_SIZE)
            sharedFeed.set(image)
        except:
            print("Failed to receive...")

##############################
# Send function
##############################

def tcpSender():
    while(1):
        try:
            if detected == 1:
                Pack = struct.pack('hh', yawC.get(), pitchC.get())
                print("sending commands..")
                net.Send(packet)
                print("commands sent")
        except:
            print("Failed to send...")

##############################
# Image Processing function
##############################

def imageProcessProcess():
    DAmount = 0
    time.sleep(5)
    while(1):
        # print("here")
        c1, c2, d1, d2 = analysis.drone_detection(sharedFeed.get())
        if d1 and d2 == 0:
            DAmount = 0
            detected.set(0)
        else:
            DAmount = DAmount + 1
        if DAmount > 4:
            # print(w,h,c1,c2)
            center1.set(c2)
            center2.set(c1)
            drone1.set(d1)
            drone2.set(d2)
            print("Setting True")
            detected.set(1)
            print("Setting True")

##############################
# Motor Correction function
##############################

def McCorrection():
    correctionList = 0
    print()
    while(1):
        if detected.get() == 1:
            print("HEJ")
            if created.get() == 1:
                print("1")
                imgList = [center1.get(), center2.get(), drone1.get(), drone2.get()]
                print(imgList)
                yawC, pitchC = correction.motorCorrection(imgList, 53, 4,correctionList,0,0)
                print(yawC)
            else:
                created.set(1)
                yawC, pitchC = correction.motorCorrection(imgList, 53, 4,correctionList,0,0)
                with open('McC/correctionList.pkl', 'rb') as f:
                    correctionList = pickle.load(f)

##############################################################
# Main
##############################################################

if __name__ == '__main__':
    try:
        sendProcess = mp.Process(target=tcpSender,)
        receiveProcess = mp.Process(target=Receiver, args=(bufferSize,))
        imgProcessor = mp.Process(target=imageProcessProcess,)
        McCProcess = mp.Process(target=McCorrection,)

        receiveProcess.start()
        sendProcess.start()
        imgProcessor.start()
        McCProcess.start()
        receiveProcess.join()
        sendProcess.join()
        imgProcessor.join()
        McCProcess.join()
    except KeyboardInterrupt:
        print("Shutting down....")
        sendProcess.terminate()
        receiveProcess.terminate()
        imgProcessor.terminate()
        McCProcess.terminate()
        print("Bye")
