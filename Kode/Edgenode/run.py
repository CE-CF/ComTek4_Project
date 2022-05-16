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
    connect = 0
    while(1):
        try:
            if detected.get() == 1:
                packet = struct.pack('hh', yawC.get(), pitchC.get())
                #print("sending commands..")
                net.tcpSend(packet,connect)
                #print("commands sent")
                connect = 1
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
            #print(c1,c2,d1, d2)
            center1.set(c2)
            center2.set(c1)
            drone1.set(d1)
            drone2.set(d2)
            detected.set(1)

##############################
# Motor Correction function
##############################

def McCorrection():
    correctionList = 0
    while(1):
        # print(f'detected: {detected.get()}')
        if detected.get() == 1:
            # print(f'created: {created.get()}')
            if created.get() != 1:
                created.set(1)
                imgList = [center1.get(), center2.get(), drone1.get(), drone2.get()]
                yaw, pitch = correction.motorCorrection(imgList, 53, 4,correctionList,1,0)
                yawC.set(yaw)
                pitchC.set(pitch)
                with open("/home/madss/Documents/school/4S/projekt/ComTek4_Project/correctionList.pkl", 'rb') as f:
                    correctionList = pickle.load(f)
            else: 
                imgList = [center1.get(), center2.get(), drone1.get(), drone2.get()]
                print(imgList)
                yaw, pitch = correction.motorCorrection(imgList, 53, 4,correctionList,1,0)
                yawC.set(yaw)
                pitchC.set(pitch)
  

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
