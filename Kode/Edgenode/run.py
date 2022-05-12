import WiFi.WiFi
import ImgProcess.Img_process as analysis
import McC.McC as correction
import multiprocessing as mp
import socket, time, struct, math
import numpy as np
import cv2


##############################################################
# Renaming
##############################################################

net = WiFi.WiFi
manager = mp.Manager()

##############################################################
# Variables
##############################################################

bufferSize = 100000

##############################################################
# Variables: Shared memory
##############################################################

sharedFeed = manager.Value(bytes, 0xff)
detected = manager.Value(bool, False)
created = manager.Value(int, 0)

Height = manager.Value(int, 0)
Width = manager.Value(int, 0)
center1 = manager.Value(int, 0)
center2 = manager.Value(int, 0)

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
            if detected == True:
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
    while(1):
        if c1 and c2 == 0:
            DAmount = 0
            detected.set(False)
        else:
            DAmount = DAmount + 1
            if DAmount > 4:
                w, h, c1, c2 = analysis.drone_detection(sharedFeed.get())
                Height.set(h)
                Width.set(w)
                center1.set(c1)
                center2.set(c2)
                detected.set(True)

##############################
# Motor Correction function
##############################

def McCorrection():
    while(1):
        if detected.get() == True:
            imgList = [Width.get(), Height.get(), center1.get(), center2.get()]
            yawC, pitchC = correction.motorCorrection(imgList, 53, 4,created.get(),0)
            if created.get() == 0:
                created.set(1)

##############################################################
# Main
##############################################################

if __name__ == '__main__':
    try:
        sendProcess = mp.Process(target=tcpSender,)
        receiveProcess = mp.Process(target=Receiver, args=(bufferSize))
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
